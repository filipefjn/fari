<template>
<div>
    <LoadingPage v-if="loading"/>
    <MainPage v-else/>
    <!-- <div v-if="loading">Loading!</div>
    <div v-else>
        <div v-if="currentSongInfo">
            <span>Currently playing: <b>{{currentSongInfo.tags.tracktitle}}</b> by <b>{{currentSongInfo.tags.artist}}</b></span>
            <progress :value="progressBarValue" max="100" @click="progressBarClick($event)" @drag="progressBarDrag($event)"></progress>
        </div>
        <div>
            <button @click="pausePlayer()">pause</button>
            <button @click="unpausePlayer()">play</button>
            {{cPlaybackTime}} / {{cPlaybackDuration}}
        </div>
        <div>Current dir: {{currentDir}}</div>
        <table>
            <tr v-if="currentDir !== '/'">
                <td><button @click="openSubfolder('..')">&lt;-</button></td>
                <td>..</td>
            </tr>
            <tr v-for="item in subfolders" :key="item">
                <td><button @click="openSubfolder(item)">open</button></td>
                <td>{{item}}</td>
            </tr>
            <tr v-for="item in files" :key="item">
                <td><button @click="fetchSong(item)">play</button></td>
                <td>{{item}}</td>
            </tr>
        </table>
    </div> -->
</div>
</template>

<script>
import LoadingPage from '@/pages/LoadingPage.vue';
import MainPage from '@/pages/MainPage.vue';

export default {
    name: 'app',
    components: {
        LoadingPage,
        MainPage
    },
    data: function() {
        return {
            currentDir: '/',
            subfolders: null,
            files: null,
            loading: true,
            player: null,
            playbackTime: null,
            playbackDuration: null,
            currentSongInfo: null,
            progressBarValue: 0,
        };
    },
    created: function() {
        setTimeout(() => {
            // timeout to display the LoadingPage
            this.createPlayer();
            this.fetchFolderContent();
        }, 1000);

    },
    computed: {
        cPlaybackTime: function() {
            if(!this.playbackTime) {
                return "0:00";
            } else {
                return this.formatPlaybackTime(this.playbackTime);
            }
        },
        cPlaybackDuration: function() {
            if(!this.playbackDuration) {
                return "0:00";
            } else {
                return this.formatPlaybackTime(this.playbackDuration);
            }
        }
    },
    methods: {
        createPlayer: function() {
            this.player = new window.Audio();
            this.player.addEventListener('play', (event) => {
                console.log('started playback');
            });
            this.player.addEventListener('pause', (event) => {
                console.log('paused playback');
            });
            this.player.addEventListener('durationchange', (event) => {
                this.playbackDuration = this.player.duration;
            });
            setInterval(() => {
                this.playbackTime = this.player.currentTime;
                this.updateProgressBar();
            }, 250);

        },
        fetchFolderContent: function() {
            fetch('/api/folder-content', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    path: this.currentDir,
                })
            }).then((response) => {
                return response.json();
            }).then((response) => {
                this.subfolders = response.subfolders;
                this.files = response.files;
                this.loading = false;
            })
        },
        openSubfolder: function(path) {
            this.loading = true;
            this.subfolders = null;
            this.files = null;
            if(path == '..') {
                this.currentDir = this.currentDir.split('/').reverse().slice(2).reverse().join('/') + "/";
                if(!this.currentDir) {
                    this.currentDir = "/";
                }
            } else {
                this.currentDir = this.currentDir + path + "/";
            }
            this.fetchFolderContent();
        },
        fetchSong: function(file) {
            let filePath = this.currentDir + file; // + "/"
            console.log('fetching song ' + file)
            this.fetchSongInfo(filePath);
            this.fetchSongData(filePath);
        },
        fetchSongInfo: function(filePath) {
            fetch('/api/file-info', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    path: filePath,
                })
            }).then((response) => {
                if(response.status !== 200) {
                    console.error("response status: " + response.status);
                    return;
                } else {
                    response.json().then((json_response) => {
                        console.log(json_response);
                        this.currentSongInfo = json_response;
                    })
                }
                return
            })
        },
        fetchSongData: function(filePath) {
            fetch('/api/fetch-file', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    path: filePath,
                })
            }).then((response) => {
                if(response.status !== 200) {
                    console.error("response status: " + response.status);
                    return;
                } else {
                    response.blob().then((blob) => {
                        console.log(blob);
                        this.player.src = window.URL.createObjectURL(blob);
                        this.player.play();
                    })
                }
                return
            })
        },
        pausePlayer: function() {
            this.player.pause()
        },
        unpausePlayer: function() {
            this.player.play()
        },
        formatPlaybackTime: function(val) {
            val = Math.floor(val);
            let minutes = Math.floor(val / 60).toFixed();
            let seconds = (val % 60).toFixed();
            if(seconds.length == 1) {
                seconds = "0" + seconds;
            }
            return minutes + ":" + seconds;
        },
        progressBarClick: function(event) {
            let x = event.pageX - event.target.offsetLeft;
            let clickPosition = x / event.target.offsetWidth;
            this.progressBarValue = clickPosition * 100;
            this.player.currentTime = clickPosition * this.player.duration;
        },
        updateProgressBar: function() {
            let updatedPosition = this.player.currentTime / this.player.duration * 100;
            this.progressBarValue = updatedPosition;
        },
        progressBarDrag: function(event) {
            console.log(event);
        }
    }
}
</script>

<style lang="scss">
</style>
