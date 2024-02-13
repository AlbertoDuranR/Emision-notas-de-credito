<template>
  <Header />
  <div class="container px-6 mx-auto block">
    <div class="flex items-center justify-center py-5">
      <span class="font-bold text-gray-600"
        >BANDEJA DE SOLICITUDES DE NOTAS DE CRÉDITO - PUNTOS DE VENTA</span
      >
    </div>
  </div>
  <div class="px-4 flex justify-center">
    <button
      class="text-sm rounded-full bg-green-600 p-2 text-white font-bold flex"
      type="button"
    >
      <svg
        class="h-5 w-5 white"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M13 9l3 3m0 0l-3 3m3-3H8m13 0a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      &nbsp;Enviar Consolidado
    </button>
  </div>
  <TablaDetalle
    tipo="bandeja"
    :listaSolicitudes="lista_solicitudes"
    @validar_item="validar_item"
    @observar_item="observar_item"
    @generar_nota_item="generar_nota_item"
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
  name: "BNotaPDV",
  props: {
    lista_solicitudes: Array,
  },
  data() {
    return {
      isOpen: false,
      datos_detalle_solicitud: {},
      isLoadingSolicitud: false,
    };
  },
  mounted() {
    // Imprimir datos en la consola
    //console.log(this.lista_solicitudes);
  },
  methods: {
    validar_item(itemNota, nroComprobante) {
      console.log("Editar:", itemNota);

      this.$swal
        .fire({
          title: "Advertencia!",
          text: "¿Estás seguro de validar la solicitud?",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, validar",
          cancelButtonText: "Cancelar",
        })
        .then((result) => {
          if (result.isConfirmed) {
            // Lógica para la confirmación
            axios
              .post("/solicitud_nota_credito/punto_venta/validar/", {
                id: itemNota,
                nro_comprobante: nroComprobante,
              })
              .then((response) => {
                console.log(response);
                this.$swal.fire(
                  "Validado",
                  "El elemento ha sido validado.",
                  "success"
                );
                // Recargar la página completa después de eliminar
                location.reload();
              })
              .catch((err) => {
                const msg_error = err.response.data.message;
                this.$swal.fire({
                  title: "Error de Validación",
                  text: `${msg_error}`,
                  icon: "error",
                });
                location.reload();
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
    observar_item(item_nota) {
      this.$swal
        .fire({
          title: "Observar solicitud",
          text: "Ingresa la observación",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, observar",
          cancelButtonText: "Cancelar",
          input: "textarea", // Cambiar a un campo de entrada de texto tipo textarea
          inputAttributes: {
            placeholder: "Describe la observación", // Título del campo de entrada
            rows: 3, // Altura del textarea (puedes ajustar este valor según tus necesidades)
          },
        })
        .then((result) => {
          if (result.isConfirmed) {
            console.log(result);
            // Verificar si se ingresó un texto
            if (result.value == "" || result.value === null) {
              this.$swal.fire({
                title: "Error",
                text: "Debes ingresar una razón para observar la solicitud.",
                icon: "error",
              });
            } else {
              // Lógica para la observación
              axios
                .post("/solicitud_nota_credito/punto_venta/observacion/", {
                  id: item_nota,
                  observacion: result.value, // Agregar la razón al objeto que envías al servidor
                })
                .then((response) => {
                  console.log(response);
                  this.$swal.fire(
                    "Observar",
                    "El elemento ha sido observado y será enviado a verificación.",
                    "success"
                  );
                  // Recargar la página completa después de observar
                  location.reload();
                })
                .catch((err) => {
                  console.log(err);
                  this.$swal.fire({
                    title: "Error de Registro",
                    text: "Error al Observar datos",
                    icon: "error",
                  });
                });
            }
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
    generar_nota_item(item_nota) {
      this.$swal
        .fire({
          title: "Advertencia!",
          text: "¿Estás seguro de Generar la Nota de Crédito?",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, Generar",
          cancelButtonText: "Cancelar",
        })
        .then((result) => {
          if (result.isConfirmed) {
            // Lógica para la confirmación
            axios
              .post("/nota_credito/punto_venta/create/", {
                id: item_nota,
                estado: "VALIDADO",
              })
              .then((response) => {
                console.log(response);
                this.$swal.fire("CREADO", "Nota de crédito CREADA", "success");
                // Recargar la página completa
                location.reload();
              })
              .catch((err) => {
                console.log(err);
                Swal.fire({
                  title: "Error de Registro",
                  text: "Error al crear la Nota de Crédito",
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
