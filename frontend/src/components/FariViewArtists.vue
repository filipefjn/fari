<template>
    <div class="container">
        <div ref="topRef"></div>
        <FariList v-if="!selectedArtist">
            <FariRowSimple
                v-for="artist in artistList"
                :key="artist.id"
                @click="onArtistClick(artist)"
            >{{artist.name}}</FariRowSimple>
        </FariList>
        <FariList v-if="selectedArtist">
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

            <div style="display: flex; flex-direction: column"
                v-for="album in selectedArtist.albums" :key="album.id"
            >
                <FariRowAlbum
                    :albumId="album.id"
                    :title="album.name"
                    :artist="selectedArtist.name"
                    :year="album.year"
                />
                <FariRowSong v-for="song in album.songs"
                    :song="song"
                    :key="song.id"
                    @click="onSongClick(song)"
                    @playSong="playSong(song)"
                    @change="reloadArtistInfo(selectedArtist)"
                    showTracknumber
                    showRating
                ></FariRowSong>
            </div>
        </FariList>
    </div>
</template>

<script>
import FariList from '@/components/FariList.vue';
import FariRowSong from '@/components/FariRowSong.vue';
import FariRowSimple from '@/components/FariRowSimple.vue';
import FariRowAlbum from '@/components/FariRowAlbum.vue';
import FariRowIcon from '@/components/FariRowIcon.vue';

import { mapGetters, mapActions } from 'vuex';
import { shuffle } from 'lodash';

export default {
    components: {
        FariList,
        FariRowSong,
        FariRowSimple,
        FariRowAlbum,
        FariRowIcon
    },
    data: function() {
        return {
            artistList: [],
            selectedArtist: null,
            isSelectedArtist: false,
        };
    },
    created: function() {
        this.fetchArtistList();
    },
    computed: {
        ...mapGetters(['fullSongList', 'tagList']),
    },
    activated: function() {
        this.setHeaderInfo();
        this.setDisplayNavigationButtons(true);
        if(this.isSelectedArtist) {
            this.setBackButtonAction(this.onGoBackClick);
        }
    },
    deactivated: function() {
        this.resetBackButtonAction();
    },
    methods: {
        ...mapActions(['setFullSongListPendingRefresh', 'setBackButtonAction', 'resetBackButtonAction', 'setDisplayNavigationButtons']),
        fetchArtistList: function() {
            fetch('/api/artist-list', {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(async (response) => {
                if(response.status === 200) {
                    let responseData = await response.json();
                    this.artistList = responseData;
                }
            });
        },
        onSongClick: function(song) {
            if(!song.enabled) {
                return;
            } else {
                this.playSong(song);
            }
        },
        playSong: async function(song) {
            if(!this.selectedArtist) {
                console.error("no selected artist!");
                return;
            }

            // create song list
            let songList = [];
            this.selectedArtist.albums.forEach((album) => {
                album.songs.forEach((song) => {
                    songList.push(song);
                })
            });

            let queue = [];
            let queuePlayIndex = 0;
            let offset = 0;
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
        onArtistClick: function(artist) {
            this.setBackButtonAction(this.onGoBackClick);
            this.loadArtistInfo(artist);
        },
        loadArtistInfo: function(artist) {
            this.isSelectedArtist = true;
            fetch('/api/artist-song-list', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id: artist.id
                })
            }).then(async (response) => {
                if(response.status === 200) {
                    this.selectedArtist = await response.json();
                }
            });
        },
        reloadArtistInfo: function(artist) {
            this.setFullSongListPendingRefresh();
            this.loadArtistInfo(artist)
        },
        onGoBackClick: function() {
            this.selectedArtist = null;
            this.isSelectedArtist = false;
        },
        onShuffleClick: function() {
            let shuffledList = shuffle(this.selectedArtistSongList);
            this.playSong(null, shuffledList);
        },
        setHeaderInfo: function() {
            let artistName = "";
            if(this.selectedArtist && this.selectedArtist.name) {
                artistName = this.selectedArtist.name;
            }
            this.$store.dispatch('setHeaderInfo', {
                title: "Artists",
                subtitle: artistName
            });
        }
    },
    watch: {
        selectedArtist: function(newValue, oldValue) {
            if(!oldValue && newValue) {
                // move to the top on next tick
                this.$nextTick(() => {
                    this.$refs.topRef.scrollIntoView({block: "start"});
                });
            }
            this.$nextTick(() => {
                this.setHeaderInfo();
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
