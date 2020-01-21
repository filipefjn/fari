<template>
    <div class="container">
        <div class="header">
            <div class="title">Folders</div>
            <div class="path">{{currentDir}}</div>
        </div>
        <div class="list">
            <div class="list-item" v-if="currentDir !== '/'" @click="openSubfolder('..')">
                <div class="icon"><fa-icon icon="level-up-alt"/></div>
                ..
            </div>
            <div class="list-item" v-for="item in subfolders" @click="openSubfolder(item)" :key="item">
                <div class="icon"><fa-icon icon="folder"/></div>
                {{item}}
            </div>
            <div class="list-item" v-for="item in files" :key="item" @click="fetchSong(item)">
                <div class="icon"><fa-icon icon="music"/></div>
                {{item}}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data: function() {
        return {
            currentDir: '/',
            subfolders: null,
            files: null,
            loading: true,
        };
    },
    mounted: function() {
        this.fetchFolderContent();
    },
    methods: {
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
            this.$store.dispatch('pausePlayer');
            let filePath = this.currentDir + file;
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
                    response.json().then((info) => {
                        this.$store.dispatch('setSongInfo', info);
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
                        this.$store.dispatch('playBlob', blob);
                    })
                }
                return
            })
        },
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.container {

    padding-bottom: 2rem;

    &> * {
        padding-right: 2rem;
        padding-left: 2rem;
    }

    .header {
        height: 5rem;
        display: flex;
        align-items: center;
        padding-left: 2rem;
        background-image: linear-gradient(black, rgba(0,0,0,0));
        user-select: none;
        padding-bottom: 4px;

        .title {
            font-size: 2rem;
            color: $primary;
            margin-right: 2rem;
        }
        .path {
            font-size: 1rem;
            color: $primary;
            margin-top: 0.5rem;
        }
    }

    .list {
        user-select: none;

        .list-item {
            padding-top: $list-item-hor-padding;
            padding-bottom: $list-item-hor-padding;
            padding-left: 1rem;
            padding-right: 1rem;
            border-top: solid 2px $list-item-line-color;
            color: $text-color;
            cursor: pointer;
            display: flex;
            align-items: center;

            .icon {
                margin-right: 1rem;
                font-size: 1.25rem;
                width: 1rem;
                color: $list-item-icon-color;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            &:last-child {
                border-bottom: solid 2px $list-item-line-color;
            }

            &:hover {
                background-color: $list-item-hover-bgcolor;
            }
        }
    }
}


</style>
