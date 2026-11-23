package com.evparking.usuariocarro.carro;

import com.evparking.usuariocarro.usuario.Usuario;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;

@Entity
@Table(name = "carros_usuario")
public class CarroUsuario {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Placa é obrigatória")
    private String placa;

    @NotBlank(message = "Modelo é obrigatório")
    private String modelo;

    private String marca;
    private String tipoConector;
    private Double capacidadeBateriaKwh;

    @ManyToOne(optional = false)
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getPlaca() { return placa; }
    public void setPlaca(String placa) { this.placa = placa; }

    public String getModelo() { return modelo; }
    public void setModelo(String modelo) { this.modelo = modelo; }

    public String getMarca() { return marca; }
    public void setMarca(String marca) { this.marca = marca; }

    public String getTipoConector() { return tipoConector; }
    public void setTipoConector(String tipoConector) { this.tipoConector = tipoConector; }

    public Double getCapacidadeBateriaKwh() { return capacidadeBateriaKwh; }
    public void setCapacidadeBateriaKwh(Double capacidadeBateriaKwh) { this.capacidadeBateriaKwh = capacidadeBateriaKwh; }

    public Usuario getUsuario() { return usuario; }
    public void setUsuario(Usuario usuario) { this.usuario = usuario; }
}
