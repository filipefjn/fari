<template>
    <div class="container">
        <ContentHeader title="Folders" :subtitle="currentDir"/>
        <ContentList>
            <ContentListItem v-if="currentDir !== '/'" @click="openSubfolder('..')">
                <div class="icon"><fa-icon icon="level-up-alt"/></div>
                ..
            </ContentListItem>
            <ContentListItem v-for="item in subfolders" @click="openSubfolder(item)" :key="item">
                <div class="icon"><fa-icon icon="folder"/></div>
                {{item}}
            </ContentListItem>
            <ContentListItem v-for="item in files" :key="item" @click="fetchSong(item)">
                <div class="icon"><fa-icon icon="music"/></div>
                {{item}}
            </ContentListItem>
        </ContentList>
    </div>
</template>

<script>
import ContentHeader from '@/components/ContentHeader.vue';
import ContentList from '@/components/ContentList.vue';
import ContentListItem from '@/components/ContentListItem.vue';

export default {
    components: {
        ContentHeader,
        ContentList,
        ContentListItem
    },
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

    .icon {
        margin-right: 1rem;
        font-size: 1.25rem;
        width: 1rem;
        color: $list-item-icon-color;
        display: flex;
        justify-content: center;
        align-items: center;
    }

}
</style>
