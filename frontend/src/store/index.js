import Vue from 'vue';
import Vuex from 'vuex';
import tools from '@/libs/tools.js';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        player: null,
        playerStatus: null,
        playerInfo: null,
        playerVolume: 0.8,
        fullSongList: [],
        fullSongListPendingRefresh: false,
        tagList: [],
        songInfo: null,
        songArtworkCounter: 0,
        queue: [],
        queueKeyCounter: 0, // TODO use later to update queue songs info
        queuePlayIndex: 0,
        queuePlaySongId: null,
        displayMobileSidebar: false,
        headerInfo: {},
        listParams: {},
        loadingScreen: false,
        albumArtworkList: {},
        displayNavigationButtons: false,
        backButtonAction: null
    },
    getters: {
        player: (state) => state.player,
        playerStatus: (state) => state.playerStatus,
        playerInfo: (state) => state.playerInfo,
        playerVolume: (state) => state.playerVolume,
        fullSongList: (state) => state.fullSongList,
        fullSongListPendingRefresh: (state) => state.fullSongListPendingRefresh,
        tagList: (state) => state.tagList,
        songInfo: (state) => state.songInfo,
        songArtworkCounter: (state) => state.songArtworkCounter,
        queue: (state) => state.queue,
        queueKeyCounter: (state) => state.queueKeyCounter,
        queuePlayIndex: (state) => state.queuePlayIndex,
        queuePlaySongId: (state) => state.queuePlaySongId,
        displayMobileSidebar: (state) => state.displayMobileSidebar,
        headerInfo: (state) => state.headerInfo,
        listParams: (state) => state.listParams,
        loadingScreen: (state) => state.loadingScreen,
        albumArtworkList: (state) => state.albumArtworkList,
        displayNavigationButtons: (state) => state.displayNavigationButtons,
        backButtonAction: (state) => state.backButtonAction
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
        setFullSongList: (state, fullSongList) => {
            state.fullSongList = fullSongList;
        },
        setFullSongListPendingRefresh: (state, pending) => {
            state.fullSongListPendingRefresh = pending;
        },
        setTagList: (state, tagList) => {
            state.tagList = [
                ...tagList
            ];
        },
        setSongInfo: (state, info) => {
            if(state.songInfo) {
                if(state.songInfo.artwork !== info.artwork) {
                    state.songArtworkCounter = state.songArtworkCounter + 1;
                }
            }
            state.songInfo = info;
        },
        setPlayerVolume: (state, volume) => {
            state.playerVolume = volume;
            if(state.player) {
                state.player.volume = tools.volumeInterpolation(volume);
            }
        },
        setPlayerTime: (state, timeSeconds) => {
            if(state.player) {
                state.player.currentTime = timeSeconds;
            }
        },
        appendToQueue: (state, song) => {
            let queue = {
                ...state.queue,
                song
            };
            state.queue = queue;
        },
        setQueue: (state, songArray) => {
            state.queue = songArray;
        },
        setQueuePlayIndex: (state, index) => {
            state.queuePlayIndex = index;
        },
        setQueuePlaySongId: (state, id) => {
            state.queuePlaySongId = id;
        },
        setMobileSidebar: (state, value) => {
            state.displayMobileSidebar = value;
        },
        setHeaderInfo: (state, info) => {
            state.headerInfo = {
                ...info
            };
        },
        setListParams: (state, params) => {
            state.listParams = {
                ...state.listParams,
                ...params
            };
        },
        setLoadingScreen: (state, value) => {
            state.loadingScreen = !!value;
        },
        appendAlbumArtworkList: (state, payload) => {
            state.albumArtworkList = {
                ...state.albumArtworkList,
                ...payload
            }
        },
        setDisplayNavigationButtons: (state, value) => {
            state.displayNavigationButtons = value;
        },
        setBackButtonAction: (state, action) => {
            state.backButtonAction = action;
        }
    },
    actions: {
        createPlayer: ({ commit, dispatch, getters }) => {
            let player = new window.Audio();
            player.volume = tools.volumeInterpolation(getters.playerVolume);
            player.addEventListener('play', () => {
                commit('setPlayerStatus', 'playing');
            });
            player.addEventListener('pause', () => {
                if(player.ended) {
                    commit('setPlayerStatus', 'finished');
                    commit('setQueuePlaySongId', null);
                    dispatch('playNextFromQueue', false);
                } else {
                    commit('setPlayerStatus', 'paused');
                }
            });
            let intervalId = setInterval(() => {
                let progress = player.currentTime / player.duration;
                if(!isNaN(progress)) {
                    commit('setPlayerInfo', {
                        progress: progress,
                        currentTime: player.currentTime,
                        duration: player.duration
                    });
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
        fetchFullSongList: async ({commit, getters, dispatch}, payload) => {
            if(getters.fullSongList.length === 0 && (payload && payload.force !== true)) {
                return;
            }
            let fullSongList = await fetch('/api/full-song-list', {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json"
                }
            }).then((response) => {
                return response.json();
            })
            commit('setFullSongList', fullSongList);
            if(getters.fullSongList.length === 0 && (payload && payload.force !== true)) {
                return;
            }
            await dispatch('fetchTagList');
        },
        setFullSongListPendingRefresh: ({ commit }) => {
            commit('setFullSongListPendingRefresh', true);
        },
        refreshFullSongList: async ({ commit, dispatch, getters }) => {
            if(getters.fullSongListPendingRefresh) {
                await dispatch('fetchFullSongList');
                commit('setFullSongListPendingRefresh', false);
            }
        },
        fetchTagList: async ({commit}) => {
            let setTagList = await fetch('/api/tag-list', {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json"
                }
            }).then((response) => {
                return response.json();
            })
            commit('setTagList', setTagList);
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
        },
        seekPosition: ({ commit, getters }, position) => {
            if(!getters.player) {
                return;
            }
            let duration = getters.player.duration;
            if(duration) {
                position = Math.min(position, 1);
                position = Math.max(position, 0);
                let time = position * duration;
                commit('setPlayerTime', time);
            }
        },
        appendToQueue: ({ commit }, song) => {
            commit('appendToQueue', song);
        },
        setQueue: ({ commit }, songArray) => {
            if(!Array.isArray(songArray)) {
                console.error('setQueue only accepts arrays');
                return;
            }
            commit('setQueue', songArray);
        },
        playFromQueue: async ({ commit, getters, dispatch }, index) => {
            if(!index) {
                index = 0;
            }
            if(getters.queue.length <= index) {
                console.error("playFromQueue received index out of bounds");
                return;
            }
            // get song from queue
            let song = getters.queue[index];
            // TODO check if song info already exists
            // ...
            // get song info
            let songInfo = await fetch('/api/file-info', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(song)
            });
            if(songInfo.status !== 200) {
                console.error("file-info request return " + songInfo.status);
                return;
            }
            songInfo = await songInfo.json();
            await dispatch('setSongInfo', songInfo);

            // get song data
            let songData = await fetch('/api/fetch-file', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(song)
            });
            if(songData.status !== 200) {
                console.error("file-info request return " + songData.status);
                return;
            }
            songData = await songData.blob();
            await dispatch('playBlob', songData);
            commit('setQueuePlayIndex', index);
            commit('setQueuePlaySongId', song.id);
        },
        playNextFromQueue: ({ dispatch, state }, loop = true) => {
            if(!state.queue) {
                console.warn("queue is empty");
                return;
            }
            let next = state.queuePlayIndex + 1;
            if(next >= state.queue.length) {
                if(loop) {
                    next = 0;
                } else {
                    return;
                }
            }
            dispatch('playFromQueue', next);
        },
        playPreviousFromQueue: ({ dispatch, state }) => {
            if(!state.queue) {
                console.warn("queue is empty");
                return;
            }
            if(state.player.currentTime > 5) {
                // goes back to the start of the song
                dispatch('seekPosition', 0);
            } else {
                // goes to previous song
                let previous = state.queuePlayIndex - 1;
                previous = Math.max(previous, 0);
                if(previous >= state.queue.length) {
                    previous = 0;
                }
                dispatch('playFromQueue', previous);
            }
        },
        openMobileSidebar: ({ commit }) => {
            commit('setMobileSidebar', true);
        },
        closeMobileSidebar: ({ commit }) => {
            commit('setMobileSidebar', false);
        },
        setHeaderInfo: ({ commit }, info) => {
            commit('setHeaderInfo', info);
        },
        setListParams: ({ commit }, params) => {
            commit('setListParams', params);
        },
        setLoadingScreen: ({ commit }, value) => {
            commit('setLoadingScreen', !!value);
        },
        getAlbumArtwork: async ({ commit, getters }, albumId) => {
            if(getters.albumArtworkList[albumId] !== undefined) {
                return getters.albumArtworkList[albumId];
            } else {
                let artwork = await fetch('/api/album-artwork', {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(
                        {
                            "id": albumId
                        }
                    )
                }).then((response) => {
                    if(response.status !== 200) {
                        return undefined;
                    }
                    return response.json();
                }).then((response) => {
                    if(response === undefined) {
                        return undefined;
                    }
                    if(response.artwork) {
                        return response.artwork;
                    } else {
                        return null;
                    }

                });
                if(artwork === undefined) {
                    return;
                }
                let payload = {};
                payload[albumId] = artwork;
                commit('appendAlbumArtworkList', payload);
                return artwork;
            }
        },
        setDisplayNavigationButtons: ({ commit }, value = true) => {
            commit('setDisplayNavigationButtons', !!value);
        },
        setBackButtonAction: ({ commit, dispatch }, action) => {
            // TODO check if action is a function
            if(action) {
                let actionWrapper = () => {
                    dispatch('resetBackButtonAction');
                    return action();
                };
                commit('setBackButtonAction', actionWrapper);
            }
        },
        resetBackButtonAction: ({ commit }) => {
            commit('setBackButtonAction', null);
        }

    },
    modules: {}
})
