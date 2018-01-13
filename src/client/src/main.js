import Vue from 'vue';
import iView from 'iview';
import VueSocketio from 'vue-socket.io';
import {router} from './router/index';
import store from './store';
import App from './app.vue';
import 'iview/dist/styles/iview.css';

const baseUri = 'http://127.0.0.1:8080';

Vue.use(iView);
Vue.use(VueSocketio, baseUri + '/db', {'reconnect': false});

new Vue({
    el: '#app',
    router: router,
    store: store,
    render: h => h(App),
    mounted () {
        this.$store.commit('updateMenulist');
    }
});
