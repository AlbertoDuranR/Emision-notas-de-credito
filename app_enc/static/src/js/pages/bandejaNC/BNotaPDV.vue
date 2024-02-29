<template>
  <Header :selectMarket="selectMarket"/>
  <div class="container px-6 mx-auto block">
    <div class="flex items-center justify-center py-5">
      <span class="font-bold text-gray-600"
        >BANDEJA DE SOLICITUDES DE NOTAS DE CRÉDITO - PUNTOS DE VENTA</span
      >
    </div>
  </div>
  <div class="px-4 flex justify-center gap-2">
    <button
      class="text-sm rounded-full bg-cyan-500 p-2 text-white font-bold flex"
      type="button"
      @click="validar_comprobantes"
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
      &nbsp;Validar Comprobantes de Origen
    </button>
    <button
      class="text-sm rounded-full bg-green-600 p-2 text-white font-bold flex"
      type="button"
      @click="generar_notas"
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
      &nbsp;Generar Notas de Crédito
    </button>
  </div>
  <TablaDetalle
    tipo="bandeja"
    :listaSolicitudes="lista_solicitudes"
    @validar_item="validar_item"
    @observar_item="observar_item"
    @generar_nota_item="generar_nota_item"
    @reintentar_nota_item="reintentar_nota_item"
  />
  <loading-overlay
    :active="isLoading"
    :can-cancel="true"
    :is-full-page="true"
    :color="'#dc2626'"
  >
  </loading-overlay>
  <!-- -- -->
</template>
<script setup>
import LoadingOverlay from "vue3-loading-overlay";
import axios from "axios";
import Header from "../../layouts/Header.vue";
import TablaDetalle from "../../components/TablaDetalle.vue";
</script>

<script>
export default {
  name: "BNotaPDV",
  props: {
    lista_solicitudes: Array,
    selectMarket: Object
  },
  data() {
    return {
      isOpen: false,
      datos_detalle_solicitud: {},
      isLoading: false,
    };
  },
  mounted() {
    // Imprimir datos en la consola
    // console.log(this.lista_solicitudes);
    // console.log('this.selectMarket', this.selectMarket)
  },
  methods: {
    validar_item(itemNota, nroComprobante) {
      console.log("Editar:", itemNota);
      this.$swal
        .fire({
          title: "Validar",
          text: "¿Estás seguro de validar la solicitud?",
          icon: "question",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, validar",
          cancelButtonText: "Cancelar",
        })
        .then((result) => {
          if (result.isConfirmed) {
            this.isLoading=true
            // Lógica para validar
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
                ).then(() => {
                  // Recargar la página completa
                  location.reload();
                });
              })
              .catch((err) => {
                const msg_error = err.response.data.message;
                this.$swal.fire({
                  title: "Error de Validación",
                  text: `${msg_error}`,
                  icon: "error",
                }).then(() => {
                  // Recargar la página completa
                  location.reload();
                });
              })
              .finally(() => {
                this.isLoading=false
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
    validar_comprobantes() {
      this.$swal
        .fire({
          title: "Validar",
          text: "¿Estás seguro de validar todos los comprobantes?",
          icon: "question",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, validar",
          cancelButtonText: "Cancelar",
        })
        .then((result) => {
          if (result.isConfirmed) {
            this.isLoading=true
            // Lógica para validar
            axios
              .post("/solicitud_nota_credito/punto_venta/validar_todos/", {})
              .then((response) => {
                console.log(response);
                this.$swal.fire(
                  "Validados",
                  "Elementos Validados",
                  "success"
                ).then(() => {
                  location.reload();
                });
              })
              .catch((err) => {
                const msg_error = err.response.data.message;
                this.$swal.fire({
                  title: "Error de Validación",
                  text: `${msg_error}`,
                  icon: "error",
                }).then(() => {
                  location.reload();
                });
              })
              .finally(() => {
                this.isLoading=false
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
              this.isLoading=true
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
                })
                .finally(() => {
                  this.isLoading=false
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
          title: "Generar",
          text: "¿Generar Nota de Crédito?",
          icon: "question",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, Generar",
          cancelButtonText: "Cancelar",
        })
        .then((result) => {
          if (result.isConfirmed) {
            this.isLoading=true
            // Lógica para la confirmación
            axios
              .post("/nota_credito/punto_venta/create/", {
                id: item_nota,
                estado: "VALIDADO",
              })
              .then((response) => {
                console.log(response);
                this.$swal.fire("CREADO", "Nota de crédito CREADA", "success").then(() => {
                  // Recargar la página completa
                  location.reload();
                });
              })
              .catch((err) => {
                console.log('Error', err);
                this.$swal.fire({
                  title: "Error de Registro",
                  text: `Error al crear la Nota de Crédito: ${err.response.data.message}`,
                  icon: "error",
                }).then(() => {
                  // Recargar la página completa
                  location.reload();
                });
              })
              .finally(() => {
                this.isLoading=false
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
    generar_notas() {
      this.$swal
        .fire({
          title: "Generar",
          text: "¿Generar Todas las Notas de Crédito?",
          icon: "question",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, Generar",
          cancelButtonText: "Cancelar",
        })
        .then((result) => {
          if (result.isConfirmed) {
            this.isLoading=true
            // Lógica para la confirmación
            axios
              .post("/nota_credito/punto_venta/create_all/", {})
              .then((response) => {
                console.log(response);
                this.$swal.fire("CREADO", "Notas de crédito CREADAS", "success").then(() => {
                  // Recargar la página completa
                  location.reload();
                });
              })
              .catch((err) => {
                console.log('Error', err);
                this.$swal.fire({
                  title: "Error de Registro",
                  text: `Error al crear las Notas de Crédito: ${err.response.data.message}`,
                  icon: "error",
                }).then(() => {
                  // Recargar la página completa
                  location.reload();
                });
              })
              .finally(() => {
                this.isLoading=false
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
    reintentar_nota_item(item_nota, obs_rpa_nota_credito) {
      console.log('obs_rpa: ', obs_rpa_nota_credito)
      this.$swal
        .fire({
          title: "¿Reintentar nota de crédito?",
          html: `Observación en generar nota de crédito: <br /> <p class='text-red-500 max-h-32'><i>${obs_rpa_nota_credito}</i></p>`,
          iconHtml: `
            <svg
            xmlns="http://www.w3.org/2000/svg"
            width="40"
            height="40"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#000000"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"> <path d="M2.5 2v6h6M21.5 22v-6h-6"/><path d="M22 11.5A10 10 0 0 0 3.2 7.2M2 12.5a10 10 0 0 0 18.8 4.2"/></svg>
          `,
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, Reintentar",
          cancelButtonText: "Cancelar",
        })
        .then((result) => {
          if (result.isConfirmed) {
            this.isLoading=true
            // Lógica para la confirmación
            axios
              .post("/nota_credito/punto_venta/retry/", {
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
                  title: "Error",
                  text: "Error al crear la Nota de Crédito",
                  icon: "error",
                });
              })
              .finally(() => {
                this.isLoading=false
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
