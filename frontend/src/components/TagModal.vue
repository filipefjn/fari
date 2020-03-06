<template>
    <Modal :show="show" @close="$emit('close')">
        <div class="tag-list-title">Current tags</div>
        <div class="tag-list">
            <Tag v-for="tag in currentTags" :key="tag.id" @click="untagSong(tag)">{{tag.name}}</Tag>
        </div>
        <div class="tag-list-title">Available tags</div>
        <div class="tag-list">
            <Tag v-for="tag in availableTags" :key="tag.id" @click="tagSong(tag)">{{tag.name}}</Tag>
        </div>
    </Modal>
</template>

<script>
import Tag from '@/components/Tag.vue';
import Modal from '@/components/Modal.vue';

import { mapActions, mapGetters } from 'vuex';

export default {
    props: {
        songId: {
            type: String,
            required: true
        },
        show: {
            type: Boolean,
            default: true
        }
    },
    components: {
        Tag,
        Modal
    },
    data: function() {
        return {
            currentTags: [],
            availableTags: [],
        };
    },
    watch: {
        songId: {
            handler: function() {
                this.updateTagLists();
            },
            immediate: true
        },
        fullSongList: function() {
            this.updateTagLists();
        }
    },
    computed: {
        ...mapGetters(['fullSongList','tagList'])
    },
    methods: {
        ...mapActions(['fetchFullSongList']),
        tagSong: async function(tag) {
            await fetch('/api/tag-song', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(
                    {
                        "song_id": this.songId,
                        "tag_id": tag.id
                    }
                )
            });
            this.fetchFullSongList();
            this.updateTagLists();
        },
        untagSong: async function(tag) {
            await fetch('/api/untag-song', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(
                    {
                        "song_id": this.songId,
                        "tag_id": tag.id
                    }
                )
            });
            this.fetchFullSongList();
            this.updateTagLists();
        },
        updateTagLists: function() {
            // find song
            let song = this.fullSongList.find((song) => {
                if(song.id === this.songId) {
                    return true;
                } else {
                    return false;
                }
            })

            if(song == null || this.tagList == null) {
                this.currentTags = [];
                this.availableTags = [];
            } else {
                this.currentTags = this.tagList.filter((tag) => {
                    for(let i = 0; i < song.tags.length; i++) {
                        if(tag.id === song.tags[i].id) {
                            return true;
                        }
                    }
                    return false;
                });
                this.availableTags = this.tagList.filter((tag) => {
                    for(let i = 0; i < song.tags.length; i++) {
                        if(tag.id === song.tags[i].id) {
                            return false;
                        }
                    }
                    return true;
                });
            }
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';


.tag-list {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}

.tag-list-title {
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;

    &:first-child {
        margin-top: 0;
    }
}
</style>
