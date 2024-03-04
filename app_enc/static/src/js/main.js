import {createApp, h} from 'vue';
import {createInertiaApp} from '@inertiajs/vue3';
import '../css/style.css';
import Notifications from '@kyvg/vue3-notification'
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

import PrimeVue from "primevue/config";
import Lara from "./presets/lara";
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import MultiSelect from 'primevue/multiselect'
import Calendar from 'primevue/calendar'

// const pages = import.meta.glob('./pages/**/*.vue');

const pages = import.meta.glob(['./**/*.vue'],{eager: true});
const resolvedPages = Object.keys(pages).reduce((modules, key) => {
  //const name = key.replace(/^.\/pages\/(.*)\.\w+$/, '$1');
  const name_temp = key.split("/");
  const name = name_temp[name_temp.length-1].split(".vue")[0]
  //console.log(name)
  modules[name] = pages[key].default;
  return modules;
}, {});

createInertiaApp({
    resolve: async name => {
        // return (await pages[`./pages/${name}.vue`]()).default
        return resolvedPages[name];
    },
    setup({el, App, props, plugin}) {
        const app = createApp({render: () => h(App, props)})
        app.component('DataTable', DataTable)
        app.component('Column', Column)
        app.component('Button', Button);
        app.component('InputText', InputText)
        app.component('MultiSelect', MultiSelect)
        app.component('Calendar', Calendar)
        app.use(PrimeVue, { ripple: true , unstyled: true, pt: Lara });
        app.use(plugin)
        app.use(Notifications)
        app.use(VueSweetalert2);
        app.mount(el)
    },
})


// const pages = import.meta.glob('./pages/**/*.vue');
// createInertiaApp({
//     resolve: async name => {
//         return (await pages[`./pages/${name}.vue`]()).default
//     },
//     setup({el, App, props, plugin}) {
//         const app = createApp({render: () => h(App, props)}).use(router)
//         app.use(plugin)
//         app.mount(el)
//     },
// })