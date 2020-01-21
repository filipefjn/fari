import Vue from 'vue'
import App from './App.vue'
import store from './store'

// font awesome icons
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlay, faPause, faForward, faBackward, faFolder, faLevelUpAlt, faMusic, faVolumeUp } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faPlay, faPause, faForward, faBackward, faFolder, faLevelUpAlt, faMusic, faVolumeUp);

Vue.component('fa-icon', FontAwesomeIcon);

Vue.config.productionTip = false

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
