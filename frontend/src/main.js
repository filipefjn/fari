import Vue from 'vue';
import App from './App.vue';
import store from './store';
import axios from 'axios';

// font awesome icons
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlay, faPause, faForward, faBackward, faFolder, faLevelUpAlt, faMusic, faVolumeUp, faBars, faChevronUp, faChevronDown, faEllipsisH, faPlus, faTags, faArrowLeft, faRandom, faCompressArrowsAlt, faCaretLeft, faCaretRight } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import router from './router';

library.add(faPlay, faPause, faForward, faBackward, faFolder, faLevelUpAlt, faMusic, faVolumeUp, faBars, faChevronUp, faChevronDown, faEllipsisH, faPlus, faTags, faArrowLeft, faRandom, faCompressArrowsAlt, faCaretLeft, faCaretRight);

Vue.component('fa-icon', FontAwesomeIcon);

Vue.config.productionTip = false;

Vue.prototype.$http = axios;

new Vue({
    store,
    router,
    render: h => h(App)
}).$mount('#app');
