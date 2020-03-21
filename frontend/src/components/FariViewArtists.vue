<template>
    <div class="container">
        <FariList v-if="!isArtistSelected">
            <FariRowSimple
                v-for="(artist, artistKey) in artistList"
                :key="artistKey"
                @click="onArtistClick(artistKey)"
            >{{artistKey}}</FariRowSimple>
        </FariList>
        <FariList v-if="isArtistSelected">
            <!-- go back row -->
            <FariRowSimple
                @click="onGoBackClick()"
                ref="goBackRow"
            ><FariRowIcon><fa-icon icon="arrow-left"/></FariRowIcon>
            Back to artists</FariRowSimple>

            <!-- shuffle row -->
            <FariRowSimple
                @click="onShuffleClick()"
            ><FariRowIcon><fa-icon icon="random"/></FariRowIcon>
            Shuffle and play</FariRowSimple>

            <!-- song rows -->
            <FariRowSong v-for="song in selectedArtistSongList"
                :songId="song.id"
                :key="song.id"
                @click="onSongClick(song)"
                @playSong="playSong(song)"
            ></FariRowSong>
        </FariList>
    </div>
</template>

<script>
import FariList from '@/components/FariList.vue';
import FariRowSong from '@/components/FariRowSong.vue';
import FariRowSimple from '@/components/FariRowSimple.vue';
import FariRowIcon from '@/components/FariRowIcon.vue';

import { mapGetters, mapActions } from 'vuex';
import { shuffle } from 'lodash';

export default {
    components: {
        FariList,
        FariRowSong,
        FariRowSimple,
        FariRowIcon
    },
    data: function() {
        return {
            isArtistSelected: false,
            selectedArtistKey: "",
        };
    },
    computed: {
        ...mapGetters(['fullSongList', 'tagList']),
        artistList: function() {
            let list = {};
            for (let i = 0; i < this.fullSongList.length; i++) {
                let song = this.fullSongList[i];
                let songArtist = song["artist"];
                if(!list[songArtist]) {
                    list[songArtist] = [];
                }
                list[songArtist].push(song);
            }
            list = Object.keys(list).sort().reduce((r, k) => (r[k] = list[k], r), {});
            return list;
        },
        selectedArtistSongList: function() {
            return this.artistList[this.selectedArtistKey];
        }
    },
    activated: function() {
        this.$store.dispatch('setHeaderInfo', {
            title: "Artists",
        });
    },
    methods: {
        ...mapActions(['fetchFullSongList']),
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
                songList = this.selectedArtistSongList;
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
        onArtistClick: function(artistKey) {
            this.selectedArtistKey = artistKey;
            this.$nextTick(() => {
                this.isArtistSelected = true;
                this.$store.dispatch('setHeaderInfo', {
                    title: "Artists",
                    subtitle: artistKey
                });
                this.$nextTick(() => {
                    this.$refs.goBackRow.$el.scrollIntoView({block: "start"});
                });
            });
        },
        onGoBackClick: function() {
            this.isArtistSelected = false;
            this.$nextTick(() => {
                this.selectedArtistKey = "";
                this.$store.dispatch('setHeaderInfo', {
                    title: "Artists",
                    subtitle: ""
                });
            });
        },
        onShuffleClick: function() {
            let shuffledList = shuffle(this.selectedArtistSongList);
            this.playSong(null, shuffledList);
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
}

</style>
