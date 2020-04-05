<template>
    <FariModal :show="show" @close="$emit('close')">
        <FariModalTitle>Current tags</FariModalTitle>
        <FariModalSection>
            <FariTag v-for="tag in currentTags" :key="tag.id" @click="untagSong(tag)">{{tag.name}}</FariTag>
        </FariModalSection>
        <FariModalTitle>Create new tag</FariModalTitle>
        <FariModalSection>
            <FariInput :buttons="[{text: 'Create', emit: 'create'}]" @create="onCreateClick()"/>
        </FariModalSection>
        <FariModalTitle>Available tags</FariModalTitle>
        <FariModalSection>
            <FariTag v-for="tag in availableTags" :key="tag.id" @click="tagSong(tag)">{{tag.name}}</FariTag>
        </FariModalSection>
    </FariModal>
</template>

<script>
import FariTag from '@/components/FariTag.vue';
import FariModal from '@/components/FariModal.vue';
import FariModalSection from '@/components/FariModalSection.vue';
import FariModalTitle from '@/components/FariModalTitle.vue';
import FariInput from '@/components/FariInput.vue';

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
        FariTag,
        FariModal,
        FariModalSection,
        FariModalTitle,
        FariInput
    },
    data: function() {
        return {
            currentTags: [],
            availableTags: [],
            createTagValue: ""
        };
    },
    watch: {
        songId: {
            handler: function() {
                this.updateTagLists();
            },
            immediate: true
        },
        tagList: function() {
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
        },
        onCreateClick: async function() {
            // TODO improve
            if(this.createTagValue) {
                let createTagResponse = await fetch('/api/create-tag', {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(
                        {
                            "name": this.createTagValue,
                        }
                    )
                });
                if(createTagResponse.status === 201) {
                    let createTagResponseData = await createTagResponse.json();
                    this.tagSong(createTagResponseData);
                }
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
