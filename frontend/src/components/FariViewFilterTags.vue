<template>
    <div class="container">
        <div class="tag-grid">
            <div class="grid-item include-tags">
                <div class="title">Include</div>
                <div class="box">
                    <FariTag
                    v-for="tag in includeTagList"
                    :key="tag.id"
                    @click="removeIncludeTag(tag)"
                >{{tag.name}}</FariTag>
                </div>
            </div>
            <div class="grid-item exclude-tags"> <!-- TODO implement -->
                <div class="title">Exclude</div>
                <div class="box">
                    <FariTag v-for="tag in excludeTagList" :key="tag.id">{{tag.name}}</FariTag>
                </div>
            </div>
            <div class="grid-item available-tags">
                <div class="title">Available</div>
                <div class="box">
                    <FariTag
                        v-for="tag in availableTags"
                        :key="tag.id"
                        @click="addIncludeTag(tag)"
                    >{{tag.name}}</FariTag>
                </div>
            </div>
        </div>
        <FariList v-if="displayResults">
            <FariRowSimple
                @click="onShuffleClick()"
            ><FariRowIcon><fa-icon icon="random"/></FariRowIcon>
            Shuffle and play</FariRowSimple>
            <FariRowSongId v-for="song in filteredSongList"
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
import FariRowSimple from '@/components/FariRowSimple.vue';
import FariRowSongId from '@/components/FariRowSongId.vue';
import FariTag from '@/components/FariTag.vue';
import FariRowIcon from '@/components/FariRowIcon.vue';

import { mapGetters, mapActions } from 'vuex';
import { shuffle } from 'lodash';

export default {
    components: {
        FariList,
        FariRowSimple,
        FariRowSongId,
        FariTag,
        FariRowIcon
    },
    data: function() {
        return {
            includeTagList: [],
            excludeTagList: []
        };
    },
    activated: function() {
        this.setDisplayNavigationButtons(false);
        this.$store.dispatch('setHeaderInfo', {
            title: "Filter by tags"
        });
        this.refreshFullSongList();
    },
    computed: {
        ...mapGetters(['tagList', 'fullSongList']),
        displayResults: function() {
            if(!!this.includeTagList.length || !!this.excludeTagList.length) {
                return true;
            }
            return false;
        },
        availableTags: function() {
            return this.tagList.filter((tag) => {
                for(let i = 0; i < this.includeTagList.length; i++) {
                    if(tag.id === this.includeTagList[i].id) {
                        return false;
                    }
                }
                for(let i = 0; i < this.excludeTagList.length; i++) {
                    if(tag.id === this.excludeTagList[i].id) {
                        return false;
                    }
                }
                return true;
            });
        },
        filteredSongList: function() {
            let filteredList = this.fullSongList.filter((song) => {
                let valid = true;
                for(let i = 0; i < this.includeTagList.length; i++) {
                    let found = false;
                    for(let j = 0; j < song.tags.length; j++) {
                        if(this.includeTagList[i].id === song.tags[j].id) {
                            found = true;
                            break;
                        }
                    }
                    if(!found) {
                        valid = false;
                        break
                    }
                }
                return valid;
            });
            return filteredList;
        }
    },
    methods: {
        ...mapActions(['refreshFullSongList', 'setDisplayNavigationButtons']),
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
                songList = this.filteredSongList;
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
            let shuffledList = shuffle(this.filteredSongList);
            this.playSong(null, shuffledList);
        },
        addIncludeTag: function(tag) {
            this.includeTagList.push(tag);
        },
        removeIncludeTag: function(tag) {
            this.includeTagList = this.includeTagList.filter((includeTag) => {
                if(includeTag.id === tag.id) {
                    return false;
                }
                return true;
            });
        }
    },
    watch: {
        tagList: function() {
            this.includeTagList = [];
            this.excludeTagList = [];
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.container {
    overflow: hidden;

    .tag-grid {
        display: grid;
        width: 100%;
        grid-template-columns: 50% 50%;
        padding: 0 2rem;
        margin-bottom: 1rem;

        @include breakpoint(mobile) {
            padding: 0 0.5rem;
        }

        .grid-item {
            display: flex;
            flex-direction: column;

            .title {
                color: $text-color;
                padding: 0 0.75rem;
                margin-top: 0.25rem;
            }

            .box {
                display: flex;
                flex-wrap: wrap;
                background-color: rgb(43, 43, 43);
                padding: 0.5rem 0.75rem;
                margin: 0.5rem;
                border-radius: 6px;
                min-height: 3rem;
                flex-grow: 1;
                flex-shrink: 1;
            }
        }

        .available-tags {
            grid-column-end: span 2;
        }

    }

}

</style>
