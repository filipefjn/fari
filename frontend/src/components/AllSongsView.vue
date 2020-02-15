<template>
    <div class="container">
        <ContentList>
            <ContentListItemGrid v-for="item in songs" :key="item.id" @click="onSongClick(item.path)">
                <template v-slot:left>
                    <div class="icon"><fa-icon icon="play"/></div>
                </template>
                <div class="tracktitle">Control</div>
                <div class="artist">Puddle of Mudd</div>
            </ContentListItemGrid>
        </ContentList>
    </div>
</template>

<script>
import ContentList from '@/components/ContentList.vue';
import ContentListItemGrid from '@/components/ContentListItemGrid.vue';

export default {
    components: {
        ContentList,
        ContentListItemGrid
    },
    data: function() {
        return {
            loading: true,
            songs: [],
        };
    },
    mounted: function() {
        this.fetchAllSongs();
    },
    methods: {
        fetchAllSongs: function() {
            fetch('/api/all-songs', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                }
            }).then((response) => {
                return response.json();
            }).then((response) => {
                this.songs = response;
                console.log(response);
            })
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
        onSongClick: async function(path) {
            let queue = [];
            let queuePlayIndex = 0;
            for(let i = 0; i < this.songs.length; i++) {
                if(this.songs[i].path == path) {
                    queuePlayIndex = i;
                }
                queue.push({
                    path: this.songs[i].path
                });
            }
            await this.$store.dispatch('setQueue', queue);
            await this.$store.dispatch('playFromQueue', queuePlayIndex);
        },
    },
    watch: {
        currentDir: {
            handler: function(val) {
                this.$store.dispatch('setHeaderInfo', {
                    title: "Folders",
                    subtitle: val
                })
            },
            immediate: true
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.container {

    .icon {
        margin-right: 1rem;
        font-size: 1.25rem;
        width: 1rem;
        color: $list-item-icon-color;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .tracktitle {
        grid-column: 1 / 5;
    }

    .artist {
        grid-column: 5 / 11;
    }

}
</style>
