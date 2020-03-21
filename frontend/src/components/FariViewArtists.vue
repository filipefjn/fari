<template>
    <div class="container">
        <ContentList v-if="!isArtistSelected">
            <SimpleRow
                v-for="(artist, artistKey) in artistList"
                :key="artistKey"
                @click="onArtistClick(artistKey)"
            >{{artistKey}}</SimpleRow>
        </ContentList>
        <ContentList v-if="isArtistSelected">
            <SimpleRow
                @click="onGoBackClick()"
                ref="goBackRow"
            ><div class="icon"><fa-icon icon="arrow-left"/></div>
            Back to artists</SimpleRow>
            <SongRow v-for="song in selectedArtistSongList"
                :songId="song.id"
                :key="song.id"
                @click="onSongClick(song)"
                @playSong="playSong(song)"
            ></SongRow>
        </ContentList>
    </div>
</template>

<script>
import ContentList from '@/components/ContentList.vue';
import SongRow from '@/components/SongRow.vue';
import SimpleRow from '@/components/SimpleRow.vue';

import { mapGetters, mapActions } from 'vuex';

export default {
    components: {
        ContentList,
        SongRow,
        SimpleRow
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
        playSong: async function(song) {
            let queue = [];
            let queuePlayIndex = 0;
            let offset = 0;
            for(let i = 0; i < this.selectedArtistSongList.length; i++) {
                if(!this.selectedArtistSongList[i].enabled) {
                    offset++;
                    continue;
                }
                if(this.selectedArtistSongList[i].id == song.id) {
                    queuePlayIndex = i - offset;
                }
                queue.push(this.selectedArtistSongList[i]);
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
