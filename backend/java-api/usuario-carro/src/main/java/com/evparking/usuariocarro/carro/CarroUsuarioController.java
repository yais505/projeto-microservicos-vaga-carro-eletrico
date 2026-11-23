package com.evparking.usuariocarro.carro;

import com.evparking.usuariocarro.usuario.UsuarioRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@CrossOrigin(origins = "*")
public class CarroUsuarioController {

    private final CarroUsuarioRepository carroRepository;
    private final UsuarioRepository usuarioRepository;

    public CarroUsuarioController(CarroUsuarioRepository carroRepository,
                                  UsuarioRepository usuarioRepository) {
        this.carroRepository = carroRepository;
        this.usuarioRepository = usuarioRepository;
    }

    @PostMapping("/usuarios/{usuarioId}/carros")
    public ResponseEntity<?> cadastrar(@PathVariable Long usuarioId,
                                       @Valid @RequestBody CarroUsuario carro) {
        return usuarioRepository.findById(usuarioId)
                .<ResponseEntity<?>>map(usuario -> {
                    carro.setId(null);
                    carro.setUsuario(usuario);
                    CarroUsuario salvo = carroRepository.save(carro);
                    return ResponseEntity.status(HttpStatus.CREATED).body(salvo);
                })
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(Map.of("erro", "Usuário não encontrado para vincular o veículo")));
    }

    @GetMapping("/usuarios/{usuarioId}/carros")
    public List<CarroUsuario> listarPorUsuario(@PathVariable Long usuarioId) {
        return carroRepository.findByUsuarioId(usuarioId);
    }

    @GetMapping("/carros")
    public List<CarroUsuario> listarTodos() {
        return carroRepository.findAll();
    }

    @GetMapping("/carros/{id}")
    public ResponseEntity<?> buscar(@PathVariable Long id) {
        return carroRepository.findById(id)
                .<ResponseEntity<?>>map(ResponseEntity::ok)
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body(Map.of("erro", "Carro não encontrado")));
    }

    @DeleteMapping("/carros/{id}")
    public ResponseEntity<?> excluir(@PathVariable Long id) {
        if (!carroRepository.existsById(id)) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(Map.of("erro", "Carro não encontrado"));
        }
        carroRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
