<template>
    <FariModal :show="show" @close="$emit('close')">
        <FariModalTitle>Current tags</FariModalTitle>
        <FariModalSection>
            <FariTag
                v-for="tag in currentTags"
                :key="tag.id" @click="untagSong(tag)"
            >{{tag.name}}</FariTag>
        </FariModalSection>
        <FariModalTitle>Create new tag</FariModalTitle>
        <FariModalSection>
            <FariInput
                :buttons="[{text: 'Create', emit: 'create'}]"
                v-model="createTagValue"
                @create="onCreateClick()"/>
        </FariModalSection>
        <FariModalTitle>Available tags</FariModalTitle>
        <FariModalSection>
            <FariTag
                v-for="tag in availableTags"
                :key="tag.id" @click="tagSong(tag)"
            >{{tag.name}}</FariTag>
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
        song: {
            type: Object,
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
            createTagValue: ""
        };
    },
    computed: {
        ...mapGetters(['fullSongList','tagList']),
        currentTags: function() {
            if(this.song && this.song.tags) {
                return this.song.tags;
            } else {
                console.log("no current tags");
                return [];
            }
        },
        availableTags: function() {
            let currentTags = [];
            if(this.song && this.song.tags) {
                currentTags = this.song.tags;
            }
            return this.tagList.filter((tag) => {
                for(let i = 0; i < currentTags.length; i++) {
                    if(tag.id === currentTags[i].id) {
                        return false;
                    }
                }
                return true;
            });
        }
    },
    methods: {
        ...mapActions(['fetchTagList']),
        tagSong: async function(tag) {
            await fetch('/api/tag-song', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(
                    {
                        "song_id": this.song.id,
                        "tag_id": tag.id
                    }
                )
            });
            this.$emit('change');
        },
        untagSong: async function(tag) {
            await fetch('/api/untag-song', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(
                    {
                        "song_id": this.song.id,
                        "tag_id": tag.id
                    }
                )
            });
            this.$emit('change');
        },
        onCreateClick: async function() {
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
                    await this.fetchTagList();
                    // await this.tagSong(createTagResponseData);
                    this.$emit('change');
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
