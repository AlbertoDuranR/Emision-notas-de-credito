<template>
  <Header :selectMarket="selectMarket"/>
  <div class="container px-6 mx-auto block">
    <div class="flex items-center justify-center py-5">
      <span class="font-bold text-gray-600"
        >CONSOLIDADO DE NOTAS DE CRÉDITO - PUNTOS DE VENTA</span
      >
    </div>
  </div>
  <TablaDetalle
    tipo="consolidado"
    :listaSolicitudes="lista_solicitudes"
    @editar-item="editarItem"
    @eliminar-item="eliminarItem"
  />
  <!-- -- -->
</template>
<script setup>
import axios from "axios";
import Header from "../../layouts/Header.vue";
import TablaDetalle from "../../components/TablaDetalle.vue";
</script>

<script>
export default {
  name: "CNotaPDV",
  props: {
    lista_solicitudes: Array,
    selectMarket: Object
  },
  mounted() {
    // Imprimir datos en la consola
    //console.log(this.lista_solicitudes);
  },
  methods: {
    editarItem(item_nota, item_producto) {
      console.log("Editar:", item_nota, item_producto);

      this.$swal.fire({
        title: "Cargando la ventana de edición",
        text: "Espere por favor...",
        icon: "info",
        showConfirmButton: true,
        allowOutsideClick: false,
      });

      // Agregar las variables a la URL como parámetros de ruta
      this.$inertia.visit(
        `/solicitud_nota_credito/punto_venta/edit/${item_nota}/${item_producto}`,
        {
          data: {selectMarket: this.selectMarket.department_number}// Pasar los parámetros como parte del objeto de datos
        }
      );
    },
    eliminarItem(item) {
      // Lógica para eliminar el elemento (puedes implementar según tus necesidades)
      this.$swal
        .fire({
          title: "Advertencia!",
          text: "¿Estás seguro de eliminar?",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, eliminar",
          cancelButtonText: "Cancelar",
        })
        .then((result) => {
          if (result.isConfirmed) {
            // Lógica para la confirmación
            axios
              .post("/solicitud_nota_credito/punto_venta/delete/", { id: item })
              .then((response) => {
                console.log(response);
                this.$swal.fire(
                  "Eliminado",
                  "El elemento ha sido eliminado.",
                  "success"
                );
                // Recargar la página completa después de eliminar
                location.reload();
              })
              .catch((err) => {
                console.log(err);
                Swal.fire({
                  title: "Error de Registro",
                  text: "Error al Eliminar datos, verificar los campos",
                  icon: "error",
                });
              });
          } else if (result.dismiss === this.$swal.DismissReason.cancel) {
            // Lógica para la cancelación
            this.$swal.fire(
              "Cancelado",
              "No se realizó ninguna acción.",
              "info"
            );
          }
        });
    },
  },
};
</script>
<style scope></style>
