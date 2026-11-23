package com.evparking.pagamento.repository;

import com.evparking.pagamento.model.Pagamento;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface PagamentoRepository extends JpaRepository<Pagamento, Long> {
    List<Pagamento> findByUsuarioId(Long usuarioId);
}
