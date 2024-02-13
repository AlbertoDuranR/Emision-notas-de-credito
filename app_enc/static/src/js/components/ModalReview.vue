<template>
  <TransitionRoot as="template" :show="isOpen">
    <Dialog as="div" class="relative z-10" @close="isOpen = false">
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        />
      </TransitionChild>

      <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div
          class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0"
        >
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel
              class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-2xl"
            >
              <div class="bg-white px-2 pb-4 pt-5 sm:p-4 sm:pb-2">
                <div class="sm:flex sm:items-start">
                  <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                    <DialogTitle
                      as="h3"
                      class="text-base text-center font-bold leading-6 text-gray-600"
                      >DETALLE SOLICITUD</DialogTitle
                    >
                    <div class="bg-white pb-4 pt-5">
                      <div class="w-full sm:items-start">
                        <div
                          class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left"
                        >
                          <div class="mt-2">
                            <div class="columns-2 text-sm text-gray-500">
                              <b>Nro Comprobante:</b>
                              <p>
                                {{ props.detalleSolicitud.det_nro_comprobante }}
                              </p>
                            </div>
                            <div class="columns-2 text-sm text-gray-500">
                              <b>Monto Nota de crédito:</b>
                              <p>
                                {{ props.detalleSolicitud.det_importe_total }}
                              </p>
                            </div>
                            <div class="columns-2 text-sm text-gray-500">
                              <b>Motivo:</b>
                              <p>{{ props.detalleSolicitud.det_motivo }}</p>
                            </div>
                            <div class="columns-2 text-sm text-gray-500">
                              <b>Justificación:</b>
                              <p>
                                {{ props.detalleSolicitud.det_justificacion }}
                              </p>
                            </div>
                            <div class="columns-2 text-sm text-gray-500">
                              <b>Tipo Nota de Crédito:</b>
                              <p>{{ props.detalleSolicitud.sol_tipo_nc }}</p>
                            </div>
                            <div class="columns-2 text-sm text-gray-500">
                              <b>Metodo Punto de Venta:</b>
                              <p>{{ props.detalleSolicitud.det_metodo }}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="mt-2">
                      <h3 class="text-gray-500 text-center">
                        <b>Productos</b>
                      </h3>
                      <table
                        class="table-fixed w-full mt-4 border-t border-gray-300"
                        v-if="props.detalleSolicitud.productos != []"
                      >
                        <thead>
                          <tr>
                            <th
                              class="py-2 px-3 border-b text-center text-gray-500"
                            >
                              Codigo
                            </th>
                            <th
                              class="py-2 px-1 border-b text-center text-gray-500"
                            >
                              Descripción
                            </th>
                            <th
                              class="py-2 px-3 border-b text-center text-gray-500"
                            >
                              Cant.
                            </th>
                            <th
                              class="py-2 px-3 border-b text-center text-gray-500"
                            >
                              Und.
                            </th>
                            <th
                              class="py-2 px-3 border-b text-center text-gray-500"
                            >
                              Monto Total
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="item in props.detalleSolicitud.productos"
                            :key="item.codigo"
                          >
                            <td
                              class="py-2 px-4 border-b text-sm text-gray-600 text-center"
                            >
                              {{ item.codigo }}
                            </td>
                            <td
                              class="py-2 px-1 border-b text-sm text-gray-600 text-center"
                            >
                              {{ item.descripcion }}
                            </td>
                            <td
                              class="py-2 px-4 border-b text-sm text-gray-600 text-center"
                            >
                              {{ item.cantidad }}
                            </td>
                            <td
                              class="py-2 px-4 border-b text-sm text-gray-600 text-center"
                            >
                              {{ item.unidad }}
                            </td>
                            <td
                              class="py-2 px-4 border-b text-sm text-gray-600 text-center"
                            >
                              {{ item.monto_total }}
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
              <div
                class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6"
              >
                <button
                  type="button"
                  class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
                  @click="closeModal"
                  ref="cancelButtonRef"
                >
                  CERRAR
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref } from "vue";
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot,
} from "@headlessui/vue";
const props = defineProps(["open", "detalleSolicitud"]);
const isOpen = ref(props.open);
const emit = defineEmits(["show-modal"]);

const closeModal = () => {
  isOpen.value = false;
  emit("close", false);
};
</script>
