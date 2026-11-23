package com.evparking.usuariocarro.carro;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface CarroUsuarioRepository extends JpaRepository<CarroUsuario, Long> {
    List<CarroUsuario> findByUsuarioId(Long usuarioId);
}
