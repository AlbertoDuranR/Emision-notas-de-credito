import {createApp, h} from 'vue';
import {createInertiaApp} from '@inertiajs/vue3';
import '../css/style.css';
import Notifications from '@kyvg/vue3-notification'

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
        app.use(plugin)
        app.use(Notifications)
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