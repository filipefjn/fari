import Vue from 'vue';
import Vuex from 'vuex';
import tools from '@/libs/tools.js';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        player: null,
        playerStatus: null,
        playerInfo: null,
        playerVolume: 0.5,
        songInfo: null,
    },
    getters: {
        player: (state) => state.player,
        playerStatus: (state) => state.playerStatus,
        playerInfo: (state) => state.playerInfo,
        playerVolume: (state) => state.playerVolume,
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
        },
        setPlayerVolume: (state, volume) => {
            state.playerVolume = volume;
            if(state.player) {
                state.player.volume = tools.volumeInterpolation(volume);
            }
        }
    },
    actions: {
        createPlayer: ({ commit, getters }) => {
            let player = new window.Audio();
            player.volume = tools.volumeInterpolation(getters.playerVolume);
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
        },
        setPlayerVolume: ({ commit, getters }, volume) => {
            // TODO handle errors
            if(volume < 0) {
                volume = 0;
            } else if(volume > 1) {
                volume = 1;
            }
            commit('setPlayerVolume', volume);
        }
    },
    modules: {}
})
