import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        player: null,
        playerStatus: null,
        playerInfo: null,
        songInfo: null,
    },
    getters: {
        player: (state) => state.player,
        playerStatus: (state) => state.playerStatus,
        playerInfo: (state) => state.playerInfo,
        songInfo: (state) => state.songInfo
    },
    mutations: {
        setPlayer: (state, player) => {
            if(state.player) {
                delete state.player; // TODO test this
                let playerIntervalId = state.playerInfo.intervalId;
                if(playerIntervalId) {
                    clearInterval(playerIntervalId);
                }
                state.playerInfo = null;
            }
            if(player) {
                state.playerStatus = null;
            }
            state.player = player;
        },
        setPlayerStatus: (state, status) => {
            console.log('player status: ' + status); // TODO remove line
            state.playerStatus = status;
        },
        setPlayerInfo: (state, info) => {
            let currentInfo = state.playerInfo;
            if(!currentInfo) {
                currentInfo = {};
            }
            let nextInfo = {
                ...currentInfo,
                ...info
            }
            state.playerInfo = nextInfo;
        },
        clearPlayerInfo: (state) => {
            state.playerInfo = null;
        },
        setSongInfo: (state, info) => {
            state.songInfo = info;
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
            let intervalId = setInterval(() => {
                let progress = player.currentTime / player.duration;
                if(!isNaN(progress)) {
                    commit('setPlayerInfo', { progress: progress });
                }
            }, 200);
            commit('setPlayer', player);
            commit('setPlayerInfo', { intervalId: intervalId })
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
        },
        setSongInfo: ({ commit }, info) => {
            commit('setSongInfo', info);
        }
    },
    modules: {}
})
