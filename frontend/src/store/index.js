import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        player: null,
        playerStatus: null,
    },
    getters: {
        player: (state) => state.player,
        playerStatus: (state) => state.playerStatus,
    },
    mutations: {
        setPlayer: (state, player) => {
            if(state.player) {
                delete state.player;
            }
            if(player) {
                state.playerStatus = null;
            }
            state.player = player;
        },
        setPlayerStatus: (state, status) => {
            console.log('player status: ' + status); // TODO remove line
            state.playerStatus = status;
        }
    },
    actions: {
        createPlayer: ({ commit }) => {
            let player = new window.Audio();
            player.addEventListener('play', () => {
                commit('setPlayerStatus', 'playing');
            });
            player.addEventListener('pause', () => {
                if(player.ended) {
                    commit('setPlayerStatus', 'finished');
                } else {
                    commit('setPlayerStatus', 'paused');
                }
            });
            commit('setPlayer', player);
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
