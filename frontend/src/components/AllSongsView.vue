<template>
    <div class="container">
        <ContentList>
            <SongRow v-for="song in fullSongList"
                :songId="song.id"
                :key="song.id"
                @click="onSongClick(song)"
            ></SongRow>
        </ContentList>
    </div>
</template>

<script>
import ContentList from '@/components/ContentList.vue';
import SongRow from '@/components/SongRow.vue';

import { mapGetters, mapActions } from 'vuex';

export default {
    components: {
        ContentList,
        SongRow
    },
    computed: {
        ...mapGetters(['fullSongList', 'tagList']),
    },
    mounted: function() {
        this.$store.dispatch('setHeaderInfo', {
            title: "All Songs",
        });
    },
    methods: {
        ...mapActions(['fetchFullSongList']),
        onSongClick: async function(song) {
            if(!song.enabled) {
                return;
            }
            let queue = [];
            let queuePlayIndex = 0;
            let offset = 0;
            for(let i = 0; i < this.fullSongList.length; i++) {
                if(!this.fullSongList[i].enabled) {
                    offset++;
                    continue;
                }
                if(this.fullSongList[i].id == song.id) {
                    queuePlayIndex = i - offset;
                }
                queue.push({
                    path: this.fullSongList[i].path
                });
            }
            await this.$store.dispatch('setQueue', queue);
            await this.$store.dispatch('playFromQueue', queuePlayIndex);
        },
    }
}
</script>

<style>

</style>
