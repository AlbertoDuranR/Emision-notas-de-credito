<template>
  <Header />
  <div class="container px-6 mx-auto block">
    <div class="flex items-center justify-center py-5">
      <span class="font-bold text-gray-600"
        >ACTUALIZAR - SOLICITUD NOTA DE CRÉDITO - SERVICIOS - N° {{ id }}</span
      >
    </div>
    <div class="grid grid-cols-3 pt-2">
      <div class="flex"></div>
      <div class="block">
        <form action="" v-on:submit.prevent="enviarSolicitud()">
          <div class="px-4 flex justify-center">
            <button
              class="text-sm rounded-full bg-green-600 p-2 text-white font-bold flex"
              type="submit"
            >
              <svg
                class="h-5 w-5 text-white"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <line x1="12" y1="5" x2="12" y2="19" />
                <line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              &nbsp;Actualizar NC
            </button>
          </div>
          <div class="py-2">
            <span class="text-sm font-bold text-gray-600 py-5"
              >Datos de Documento de Origen</span
            >
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Fecha emisión del comprobantes:</label>
            <VueDatePicker
              v-model="datos_documento.fecha_emision.date"
            ></VueDatePicker>
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Nro. Comprobante:</label>
            <input
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              v-model="datos_documento.nro_comprobante"
            />
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Motivo:</label>
            <input
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              v-model="datos_documento.motivo"
            />
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Importe de Nota de Crédito:</label>
            <input
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              v-model="datos_documento.importe_nc"
              @input="validarImporte"
            />
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Fecha emisión de la nota de crédito:</label>
            <VueDatePicker
              v-model="datos_documento.fecha_emision_nc.date"
              
            ></VueDatePicker>
          </div>
          <div class="py-2"></div>
        </form>
      </div>
    </div>
  </div>
  <notifications />
</template>
<script setup>
// Importando layouts
import Header from "../../layouts/Header.vue";
//
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
//
import Multiselect from "vue-multiselect";
//
//
import axios from "axios";
//
import { notify } from "@kyvg/vue3-notification";
</script>
<script>
export default {
  name: "NotaServiciosEdit",
  components: { VueDatePicker, Multiselect },
  props: {
    lista_solicitudesEdit: Array,
    id: Number
  },
  data() {
    return {
      datos_documento: {
        fecha_emision: {
          date: null,
        },
        nro_comprobante: "",
        motivo: "",
        importe_nc: "",
        fecha_emision_nc: {
          date: null,
        },
      },
    };
  },
  mounted() {
    this.csrf_token = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;

    // rellenamos los campos
    this.datos_documento.fecha_emision = {
      date: new Date(`${this.lista_solicitudesEdit[0].FECHA_EMISION}T00:00:00`)
    }
    this.datos_documento.nro_comprobante = this.lista_solicitudesEdit[0].NRO_COMPROBANTE;
    this.datos_documento.motivo = this.lista_solicitudesEdit[0].MOTIVO
    this.datos_documento.importe_nc = this.lista_solicitudesEdit[0].IMPORTE_TOTAL
    this.datos_documento.fecha_emision_nc = {
      date: new Date(`${this.lista_solicitudesEdit[0].FECHA_SOLICITUD}T00:00:00`)
    };

    // imprimimos
    console.log(this.lista_solicitudesEdit[0].FECHA_EMISION);
  },
  methods: {
    //
    enviarSolicitud() {
      // Validar el campo fecha_emision
      if (!this.datos_documento.fecha_emision.date) {
        notify({
          title: "Error de Validación",
          text: "El campo fecha emision no puede ir vacío.",
          type: "error",
        });
        return;
      }

      // Validar el campo nro_comprobante
      if (this.datos_documento.nro_comprobante.length !== 13) {
        notify({
          title: "Error de Validación",
          text: "El número de comprobante debe tener una longitud de 13 caracteres.",
          type: "error",
        });
        return;
      }

      // Validar el campo motivo
      if (!this.datos_documento.motivo.trim()) {
        notify({
          title: "Error de Validación",
          text: "El campo motivo no puede ir vacío.",
          type: "error",
        });
        return;
      }

      // Validar el campo importe_nc
      const importeRegex = /^\d+(\.\d{1,2})?$/; // Expresión regular para validar números con hasta dos decimales
      if (
        !this.datos_documento.importe_nc.trim() ||
        !importeRegex.test(this.datos_documento.importe_nc.trim())
      ) {
        notify({
          title: "Error de Validación",
          text: "El campo importe_nc no puede ir vacío y contar no caracteres numericos",
          type: "error",
        });
        return;
      }

      if (!this.datos_documento.fecha_emision_nc.date) {
        notify({
          title: "Error de Validación",
          text: "El campo fecha emision de la nota de credito.",
          type: "error",
        });
        return;
      }

      let jsonString = JSON.stringify(this.$data);
      axios
        .post("/solicitud_nota_credito/servicios/create/", jsonString)
        .then((response) => {
          console.log(response);
          this.limpiarFormulario();
          notify({
            title: "Registro Exitoso",
            text: "" + response.data.message,
          });
        })
        .catch((err) => {
          console.log(err);
          notify({
            title: "Error de Registro",
            text: "Error al guardar datos verificar los campos",
            type: "error",
          });
        });
    },
    limpiarFormulario() {
      this.datos_documento = {
        fecha_emision: { date: null },
        nro_comprobante: "",
        motivo: "",
        importe_nc: "",
        fecha_emision_nc: { date: null },
      };
    },
    validarImporte() {
      // Utilizar una expresión regular para permitir solo números y opcionalmente un punto decimal
      this.datos_documento.importe_nc = this.datos_documento.importe_nc.replace(
        /[^0-9.]/g,
        ""
      );
    },

    //
  },
};
</script>
<style scope></style>
