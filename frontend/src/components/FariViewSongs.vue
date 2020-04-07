<template>
    <div class="container">
        <FariList>
            <!-- shuffle row -->
            <FariRowSimple
                @click="onShuffleClick()"
            ><FariRowIcon><fa-icon icon="random"/></FariRowIcon>
            Shuffle and play</FariRowSimple>
            <FariRowSongId v-for="song in fullSongList"
                :songId="song.id"
                :key="song.id"
                @click="onSongClick(song)"
                @playSong="playSong(song)"
            ></FariRowSongId>
        </FariList>
    </div>
</template>

<script>
import FariList from '@/components/FariList.vue';
import FariRowSongId from '@/components/FariRowSongId.vue';
import FariRowSimple from '@/components/FariRowSimple.vue';
import FariRowIcon from '@/components/FariRowIcon.vue';

import { mapGetters, mapActions } from 'vuex';
import { shuffle } from 'lodash';

export default {
    components: {
        FariList,
        FariRowSongId,
        FariRowSimple,
        FariRowIcon
    },
    computed: {
        ...mapGetters(['fullSongList', 'tagList']),
    },
    mounted: function() {
        this.$store.dispatch('setHeaderInfo', {
            title: "All Songs",
        });
    },
    activated: function() {
        this.setDisplayNavigationButtons(false);
    },
    methods: {
        ...mapActions(['fetchFullSongList', 'setDisplayNavigationButtons']),
        onSongClick: function(song) {
            if(!song.enabled) {
                return;
            } else {
                this.playSong(song);
            }
        },
        playSong: async function(song, songList = null) {
            let queue = [];
            let queuePlayIndex = 0;
            let offset = 0;
            if(!songList) {
                songList = this.fullSongList;
            }
            for(let i = 0; i < songList.length; i++) {
                if(!songList[i].enabled) {
                    offset++;
                    continue;
                }
                if(song && songList[i].id == song.id) {
                    queuePlayIndex = i - offset;
                }
                queue.push(songList[i]);
            }
            await this.$store.dispatch('setQueue', queue);
            await this.$store.dispatch('playFromQueue', queuePlayIndex);
        },
        onShuffleClick: function() {
            let shuffledList = shuffle(this.fullSongList);
            this.playSong(null, shuffledList);
        }
    }
}
</script>

<style>

</style>
