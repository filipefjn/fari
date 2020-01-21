import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        player: null,
    },
    getters: {
        player: (state) => state.player,
    },
    mutations: {
        setPlayer: (state, player) => {
            state.player = player;
        },
    },
    actions: {
        createPlayer: ({ commit }) => {
            let player = new window.Audio();
            commit('setPlayer', player);
            console.log('player created');
        },
        destroyPlayer: ({ commit }) => {
            commit('setPlayer', null);
        },
        pausePlayer: ({ commit, getters }) => {
            // TODO handle errors
            getters.player.pause();
        },
        unpausePlayer: ({ commit, getters }) => {
            // TODO handle errors
            getters.player.play();
        },
        playBlob: ({ commit, getters }, blob) => {
            let player = getters.player;
            if(player) {
                player.src = window.URL.createObjectURL(blob);
                player.play();
            } else {
                console.error('no player available');
            }
        }
    },
    modules: {}
})
