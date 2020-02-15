<template>
    <div class="container">
        <ContentList>
            <ContentListItemGrid v-for="item in songs" :key="item.id" @click="onSongClick(item)">
                <template v-slot:left>
                    <!-- <div class="icon"><fa-icon icon="play"/></div> -->
                </template>
                <div class="tracktitle">{{item.tracktitle}}</div>
                <div class="artist">{{item.artist}}</div>
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
        this.$store.dispatch('setHeaderInfo', {
            title: "All Songs",
        });
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
            })
        },
        onSongClick: async function(song) {
            if(song.disabled) {
                console.log("disabled song clicked!");
                return;
            }
            let queue = [];
            let queuePlayIndex = 0;
            for(let i = 0; i < this.songs.length; i++) {
                if(song.disabled) {
                    return;
                }
                if(this.songs[i].id == song.id) {
                    queuePlayIndex = i;
                }
                queue.push({
                    path: this.songs[i].path
                });
            }
            await this.$store.dispatch('setQueue', queue);
            await this.$store.dispatch('playFromQueue', queuePlayIndex);
        },
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
        grid-column: 1 / 7;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        padding-right: 1.5rem;
    }

    .artist {
        grid-column: 7 / 11;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }

}
</style>
