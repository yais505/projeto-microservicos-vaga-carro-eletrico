package com.evparking.pagamento.controller;

import com.evparking.pagamento.model.Pagamento;
import com.evparking.pagamento.repository.PagamentoRepository;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestClient;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/pagamentos")
@CrossOrigin(origins = "*")
public class PagamentoController {

    private final PagamentoRepository repository;
    private final RestClient restClient;

    @Value("${app.usuario-carro.url}")
    private String usuarioCarroUrl;

    @Value("${app.reserva.url}")
    private String reservaUrl;

    public PagamentoController(PagamentoRepository repository) {
        this.repository = repository;
        this.restClient = RestClient.create();
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> buscarUsuarioRemoto(Long usuarioId) {
        try {
            return restClient.get()
                    .uri(usuarioCarroUrl + "/usuarios/" + usuarioId)
                    .retrieve()
                    .body(Map.class);
        } catch (HttpClientErrorException.NotFound e) {
            return null;
        } catch (Exception e) {
            throw new IllegalStateException("Microsserviço usuario-carro indisponível na porta 8080.");
        }
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> buscarReservaRemota(Long reservaId) {
        try {
            return restClient.get()
                    .uri(reservaUrl + "/reservas/" + reservaId)
                    .retrieve()
                    .body(Map.class);
        } catch (HttpClientErrorException.NotFound e) {
            return null;
        } catch (Exception e) {
            return Map.of("aviso", "Servico reserva offline durante teste isolado");
        }
    }

    @PostMapping
    public ResponseEntity<?> registrarPagamento(@Valid @RequestBody Pagamento pagamento) {
        Map<String, Object> usuario;
        try {
            usuario = buscarUsuarioRemoto(pagamento.getUsuarioId());
        } catch (IllegalStateException ex) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("erro", ex.getMessage()));
        }

        if (usuario == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(Map.of("erro", "Usuário ID " + pagamento.getUsuarioId() + " não encontrado no serviço usuario-carro."));
        }

        Map<String, Object> reserva = buscarReservaRemota(pagamento.getReservaId());
        if (reserva == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(Map.of("erro", "Reserva ID " + pagamento.getReservaId() + " não encontrada no serviço de reservas."));
        }

        pagamento.setId(null);
        pagamento.setNomeUsuario(String.valueOf(usuario.get("nome")));
        pagamento.setStatus("APROVADO");

        Pagamento salvo = repository.save(pagamento);
        return ResponseEntity.status(HttpStatus.CREATED).body(salvo);
    }

    @GetMapping
    public List<Pagamento> listar() {
        return repository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> buscar(@PathVariable Long id) {
        return repository.findById(id)
                .<ResponseEntity<?>>map(ResponseEntity::ok)
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(Map.of("erro", "Pagamento não encontrado")));
    }

    @GetMapping("/usuario/{usuarioId}")
    public List<Pagamento> listarPorUsuario(@PathVariable Long usuarioId) {
        return repository.findByUsuarioId(usuarioId);
    }

    @PatchMapping("/{id}/estornar")
    public ResponseEntity<?> estornar(@PathVariable Long id) {
        return repository.findById(id)
                .<ResponseEntity<?>>map(p -> {
                    p.setStatus("ESTORNADO");
                    return ResponseEntity.ok(repository.save(p));
                })
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(Map.of("erro", "Pagamento não encontrado")));
    }
}
