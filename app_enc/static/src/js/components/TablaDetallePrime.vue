<template>
    <ThemeSwitcher />
    <div class="card">
        <DataTable v-model:filters="filters" v-model:selection="selectedCustomers" :value="customers" paginator :rows="10" dataKey="id" filterDisplay="menu"
            :globalFilterFields="['name', 'country.name', 'representative.name', 'balance', 'status']">
            <template #header>
                <div class="flex justify-between">
                    <Button type="button" icon="pi pi-filter-slash" label="Limpiar" outlined @click="clearFilter()" />
                    <span class="relative">
                        <i class="pi pi-search absolute top-2/4 -mt-2 left-3 text-surface-400 dark:text-surface-600" />
                        <InputText v-model="filters['global'].value" placeholder="Keyword Search"  class="pl-10 font-normal"/>
                    </span>
                </div>
            </template>
            <template #empty> No se encontraron Solicitudes. </template>
            <Column field="ID_NC" header="ID" sortable style="min-width: 1rem">
                <template #body="{ data }">
                    {{ data.ID_NC }}
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter" placeholder="Buscar por ID" />
                </template>
            </Column>
            <Column field="FECHA_CREACION" header="Fecha C. Solicitud" sortable filterField="FECHA_CREACION" dataType="date" style="min-width: 10rem">
                <template #body="{ data }">
                    {{ formatDate(data.FECHA_CREACION) }}
                </template>
                <template #filter="{ filterModel }">
                    <Calendar v-model="filterModel.value" dateFormat="mm/dd/yy" placeholder="mm/dd/yyyy" mask="99/99/9999" />
                </template>
            </Column>
            <Column header="Solicitante" sortable sortField="SOLICITANTE" filterField="SOLICITANTE" style="min-width: 14rem">
                <template #body="{ data }">
                    <span>{{ data.SOLICITANTE }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter" placeholder="Buscar por solicitante" />
                </template>
            </Column>
            <Column header="Sucursal" sortable sortField="ESTABLECIMIENTO" filterField="ESTABLECIMIENTO" style="min-width: 14rem">
                <template #body="{ data }">
                    <span>{{ data.ESTABLECIMIENTO }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter" placeholder="Search by country" />
                </template>
            </Column>
            <Column field="FECHA_EMISION" header="Fecha Comprobante" sortable filterField="FECHA_EMISION" dataType="date" style="min-width: 10rem">
                <template #body="{ data }">
                    {{ formatDate(data.FECHA_EMISION) }}
                </template>
                <template #filter="{ filterModel }">
                    <Calendar v-model="filterModel.value" dateFormat="mm/dd/yy" placeholder="mm/dd/yyyy" mask="99/99/9999" />
                </template>
            </Column>
            <Column header="Tipo Comprobante" sortable sortField="TIPO" filterField="TIPO" style="min-width: 14rem">
                <template #body="{ data }">
                    <span>{{ data.TIPO }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter" placeholder="Search by country" />
                </template>
            </Column>
            <Column header="N° Comprobante" sortable sortField="NRO_COMPROBANTE" filterField="NRO_COMPROBANTE" style="min-width: 14rem">
                <template #body="{ data }">
                    <span>{{ data.NRO_COMPROBANTE }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter" placeholder="Search by country" />
                </template>
            </Column>
            <Column header="Estado" sortable sortField="ESTADO" filterField="ESTADO" style="min-width: 14rem">
                <template #body="{ data }">
                    <span>{{ data.ESTADO}}</span>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter" placeholder="Search by country" />
                </template>
            </Column>
            <Column header="Opciones" style="min-width: 14rem">
                <template #body="{ data }">
                    <button
                        class="bg-blue-0 text-white px-2 py-1 w-1/3"
                        >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            height="19"
                            width="19"
                            viewBox="0 0 512 512"
                        >
                            <path
                            d="M441 58.9L453.1 71c9.4 9.4 9.4 24.6 0 33.9L424 134.1 377.9 88 407 58.9c9.4-9.4 24.6-9.4 33.9 0zM209.8 256.2L344 121.9 390.1 168 255.8 302.2c-2.9 2.9-6.5 5-10.4 6.1l-58.5 16.7 16.7-58.5c1.1-3.9 3.2-7.5 6.1-10.4zM373.1 25L175.8 222.2c-8.7 8.7-15 19.4-18.3 31.1l-28.6 100c-2.4 8.4-.1 17.4 6.1 23.6s15.2 8.5 23.6 6.1l100-28.6c11.8-3.4 22.5-9.7 31.1-18.3L487 138.9c28.1-28.1 28.1-73.7 0-101.8L474.9 25C446.8-3.1 401.2-3.1 373.1 25zM88 64C39.4 64 0 103.4 0 152V424c0 48.6 39.4 88 88 88H360c48.6 0 88-39.4 88-88V312c0-13.3-10.7-24-24-24s-24 10.7-24 24V424c0 22.1-17.9 40-40 40H88c-22.1 0-40-17.9-40-40V152c0-22.1 17.9-40 40-40H200c13.3 0 24-10.7 24-24s-10.7-24-24-24H88z"
                            />
                        </svg>
                    </button>
                </template>
            </Column>
            <Column field="FECHA_SOLICITUD" header="Fecha N. De Crédito" sortable filterField="FECHA_SOLICITUD" dataType="date" style="min-width: 10rem">
                <template #body="{ data }">
                    {{ formatDate(data.FECHA_SOLICITUD) }}
                </template>
                <template #filter="{ filterModel }">
                    <Calendar v-model="filterModel.value" dateFormat="mm/dd/yy" placeholder="mm/dd/yyyy" mask="99/99/9999" />
                </template>
            </Column>
            <Column header="Metodo" sortable sortField="METODO" filterField="METODO" style="min-width: 14rem">
                <template #body="{ data }">
                    <span>{{ data.METODO}}</span>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter" placeholder="Search by country" />
                </template>
            </Column>
            <Column header="Importe N. De Crédito" style="min-width: 2rem">
                <template #body="{ data }">
                    <span>{{ data.MONTO_TOTAL }}</span>
                </template>
            </Column>
            <Column header="N° N. De Crédito" sortable sortField="NRO_NOTA_CREDITO" filterField="NRO_NOTA_CREDITO" style="min-width: 14rem">
                <template #body="{ data }">
                    <span>{{ data.NRO_NOTA_CREDITO }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter" placeholder="Search by country" />
                </template>
            </Column>
            <Column header="Acepta" sortable sortField="ACEPTA" filterField="ACEPTA" style="min-width: 14rem">
                <template #body="{ data }">
                    <span>{{ data.ACEPTA }}</span>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter" placeholder="Buscar por estado" />
                </template>
            </Column>
        </DataTable>
    </div>
</template>

<script setup>
import { CustomerService } from '../service/CustomerService';

import DataTable from 'primevue/datatable';
import Column from 'primevue/column';

import { ref, onMounted } from 'vue';

import { FilterMatchMode, FilterOperator } from 'primevue/api';
// import Button from 'primevue/button';

const props = defineProps({
  "tipo": {
    type: String
  },
  "listaSolicitudes": {
    type: Array,
    required: true
  }
});

const customers = ref();
const filters = ref();
const representatives = ref([
    { name: 'Amy Elsner', image: 'amyelsner.png' },
    { name: 'Anna Fali', image: 'annafali.png' },
    { name: 'Asiya Javayant', image: 'asiyajavayant.png' },
    { name: 'Bernardo Dominic', image: 'bernardodominic.png' },
    { name: 'Elwin Sharvill', image: 'elwinsharvill.png' },
    { name: 'Ioni Bowcher', image: 'ionibowcher.png' },
    { name: 'Ivan Magalhaes', image: 'ivanmagalhaes.png' },
    { name: 'Onyama Limba', image: 'onyamalimba.png' },
    { name: 'Stephen Shaw', image: 'stephenshaw.png' },
    { name: 'XuXue Feng', image: 'xuxuefeng.png' }
]);
const statuses = ref(['unqualified', 'qualified', 'new', 'negotiation', 'renewal', 'proposal']);
const loading = ref(true);

onMounted(() => {
    // CustomerService.getCustomersMedium().then((data) => {
    //     const data2 = [
    //         {
    //             "ID_NC": 134,
    //             "ID_DETALLE": 120,
    //             // "date": "2024-01-20",
    //             "FECHA_CREACION": "2024-01-20",
    //             "USUARIO_CREADOR": null,
    //             "SOLICITANTE": "76531982 - KATERINE ESTRELLA FLORES ANGELES",
    //             "ESTABLECIMIENTO": "MARKET JR. CARAZ",
    //         },
    //         {
    //             "ID_NC": 135,
    //             "ID_DETALLE": 121,
    //             // "date": "2014-09-13",
    //             "FECHA_CREACION": "2024-02-20",
    //             "USUARIO_CREADOR": null,
    //             "SOLICITANTE": "76531982 - KATERINE ESTRELLA FLORES ANGELES",
    //             "ESTABLECIMIENTO": "MARKET JR. CARAZ",
    //         }
    //     ]
    //     customers.value = getCustomers(props.listaSolicitudes);
    //     // customers.value = getCustomers(data2);
    //     console.log('customers.value2', customers.value)
    //     loading.value = false;
    // });
    customers.value = getCustomers(props.listaSolicitudes);
    // customers.value = getCustomers(data2);
    console.log('customers.value2', customers.value)
    loading.value = false;
});


const initFilters = () => {
    filters.value = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        ID_NC: { value: null, matchMode: FilterMatchMode.CONTAINS },
        FECHA_CREACION: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
        SOLICITANTE: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        ESTABLECIMIENTO: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        FECHA_EMISION: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
        TIPO: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
        NRO_COMPROBANTE : { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        ESTADO: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
        FECHA_SOLICITUD: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
        METODO: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
        NRO_NOTA_CREDITO: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        ACEPTA: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    };

    console.log('filters.value', filters.value)
};

initFilters();

const formatDate = (value) => {
    console.log('value_date', value)
    // const value = '2018-11-21'
    // const date= new Date(value);
    return value.toLocaleDateString('en-US', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
};
const formatCurrency = (value) => {
    return value.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
};
const clearFilter = () => {
    initFilters();
};
const getCustomers = (data) => {
    return [...(data || [])].map((d) => {
        d.FECHA_CREACION = new Date(d.FECHA_CREACION);
        d.FECHA_EMISION = new Date(d.FECHA_EMISION);
        d.FECHA_SOLICITUD = new Date(d.FECHA_SOLICITUD);
        return d;
    });
};
const getSeverity = (status) => {
    switch (status) {
        case 'unqualified':
            return 'danger';

        case 'qualified':
            return 'success';

        case 'new':
            return 'info';

        case 'negotiation':
            return 'warning';

        case 'renewal':
            return null;
    }
};
</script>