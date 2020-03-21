<template>
    <div class="song-row"
        :class="{'disabled': !song.enabled, 'no-siblings': noSiblings}"
        @click="$emit('click', $event)"
        @contextmenu.prevent="$emit('contextmenu', $event)">

        <!-- Song Row -->
        <div class="song-row-info" v-if="song">
            <slot name="left"></slot>
            <div class="grid">
                <div class="tracktitle"
                    :class="{'disabled': !song.enabled, 'current': currentSong}"
                >{{song.tracktitle}}</div>
                <div class="artist"
                    :class="{'disabled': !song.enabled, 'current': currentSong}"
                >{{song.artist}}</div>
            </div>
            <div class="clickable-icon" @click.stop="() => openContextMenu($event)"><fa-icon icon="ellipsis-h"/></div>
        </div>
        <div class="song-row-tags" v-if="song && listParams.showTags">
            <Tag class="tag" v-for="tag in song.tags" :key="tag.id">{{tag.name}}</Tag>
            <div class="tag-plus-icon" @click.stop="openTagModal()"><fa-icon icon="plus"/></div>
        </div>

        <!-- Context Menu -->
        <ContextMenu
            :show="displayContextMenu"
            :posX="contextMenuPosX"
            :posY="contextMenuPosY"
            @close="closeContextMenu()"
            @mouseleave="closeContextMenu()"
        >
            <slot name="contextmenu">
                <ContextMenuItem @click.stop="contextMenuPlaySong()">Play</ContextMenuItem>
                <ContextMenuItem @click.stop="contextMenuEnableSong()">Enable</ContextMenuItem>
                <ContextMenuItem @click.stop="contextMenuDisableSong()">Disable</ContextMenuItem>
            </slot>
        </ContextMenu>

        <!-- Tag Modal -->
        <TagModal v-if="displayTagModal" :songId="songId" @close="closeTagModal()"/>
    </div>
</template>

<script>
import ContextMenu from '@/components/ContextMenu.vue';
import ContextMenuItem from '@/components/ContextMenuItem.vue';
import Tag from '@/components/Tag.vue';
import TagModal from '@/components/TagModal.vue';

import { mapGetters, mapActions } from 'vuex'

export default {
    props: {
        songId: {
            type: String,
            required: true
        },
        showTags: {
            type: Boolean
        },
        noSiblings: {
            type: Boolean,
            default: false
        }
    },
    components: {
        ContextMenu,
        ContextMenuItem,
        Tag,
        TagModal
    },
    data: function() {
        return {
            song: null,
            contextMenuPosX: 150,
            contextMenuPosY: 300,
            displayContextMenu: false,
            displayTagModal: false
        }
    },
    computed: {
        ...mapGetters(['fullSongList', 'tagList', 'listParams', 'queuePlaySongId']),
        currentSong: function() {
            if(!this.song) {
                return false;
            }
            if(this.queuePlaySongId == this.song.id) {
                return true;
            }
            return false
        }
    },
    watch: {
        songId: {
            handler: function(val) {
                this.updateSong();
            },
            immediate: true
        },
        fullSongList: function() {
            this.updateSong();
        }
    },
    methods: {
        ...mapActions(['fetchFullSongList']),
        openContextMenu: function(event) {
            this.displayContextMenu = true;
            this.contextMenuPosX = event.clientX;
            this.contextMenuPosY = event.clientY;
        },
        closeContextMenu: function() {
            this.displayContextMenu = false;
        },
        openTagModal: function() {
            this.displayTagModal = true;
        },
        closeTagModal: function() {
            this.displayTagModal = false;
        },
        updateSong: function() {
            let found = this.fullSongList.find((item) => {
                if(item.id === this.songId) {
                    return true;
                } else {
                    return false;
                }
            });
            if(found) {
                this.song = found;
            } else {
                this.song = null;
            }
        },
        contextMenuPlaySong: function() {
            this.$emit('playSong');
            this.closeContextMenu();
        },
        contextMenuEnableSong: function() {
            fetch('/api/enable-songs', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(
                    [
                        {
                            "id": this.song.id
                        }
                    ]
                )
            }).then((response) => {
                if(response.status !== 200) {
                    return;
                }
                return response.json();
            }).then((response) => {
                this.fetchFullSongList();
            });
            this.closeContextMenu();
        },
        contextMenuDisableSong: function() {
            fetch('/api/disable-songs', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(
                    [
                        {
                            "id": this.song.id
                        }
                    ]
                )
            }).then((response) => {
                if(response.status !== 200) {
                    return;
                }
                return response.json();
            }).then((response) => {
                this.fetchFullSongList();
            });
            this.closeContextMenu();
        },
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.song-row {
    display: grid;
    cursor: pointer;
    grid-template-columns: 100%;
    border-top: solid 2px $list-item-line-color;

    &:hover {
        background-color: $list-item-hover-bgcolor;
    }

    &:last-child:not(.no-siblings) {
        border-bottom: solid 2px $list-item-line-color;
    }

    &.disabled {
        cursor: not-allowed;
    }

    .song-row-info {

        padding-top: $list-item-hor-padding;
        padding-bottom: $list-item-hor-padding;
        padding-left: 1rem;
        padding-right: 1rem;
        color: $text-color;

        display: flex;
        align-items: center;
        user-select: none;

        .grid {
            display: grid;
            grid-template-columns: 10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
            flex-grow: 1;
            flex-shrink: 1;
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

        .disabled {
            color: $disabled-color;
        }

        .current {
            color: $primary;
        }
    }

    .song-row-tags {
        display: flex;
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

// TODO improve
.clickable-icon {
    font-size: 1.25rem;
    color: $list-item-icon-color;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;

    &.clickable-icon {
        margin-top: -$list-item-hor-padding;
        margin-bottom: -$list-item-hor-padding;
        padding: $list-item-clickable-icon-padding;
        border-radius: 6px;

        &:hover {
            color: $list-item-icon-hover-color;
            background-color: $list-item-icon-hover-bgcolor;
        }
    }
}

// TODO improve
.tag {
    margin-bottom: 1rem;
}

.tag-plus-icon {
    font-size: 1rem;
    color: $list-item-icon-color;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 6px;
    margin-bottom: 0.8rem;
    margin-left: 0.5rem;

    &:hover {
        color: $list-item-icon-hover-color;
        background-color: $list-item-icon-hover-bgcolor;
    }
}
</style>
