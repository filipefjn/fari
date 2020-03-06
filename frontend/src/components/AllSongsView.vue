<template>
    <div class="container">
        <ContextMenu :posX="contextMenuPosX" :posY="contextMenuPosY" :show="showContextMenu" @close="closeContextMenu()" @mouseleave="closeContextMenu()">
            <ContextMenuItem @click="onContextMenuPlay()">Play</ContextMenuItem>
            <!-- <ContextMenuItem>Play next</ContextMenuItem> -->
            <!-- <ContextMenuItem>Queue song</ContextMenuItem> -->
            <ContextMenuItem
                v-if="contextMenuSelected !== null && !contextMenuSelected.enabled"
                @click="onContextMenuEnable()">
                Enable
            </ContextMenuItem>
            <ContextMenuItem
                v-if="contextMenuSelected !== null && contextMenuSelected.enabled"
                @click="onContextMenuDisable()">
                Disable
            </ContextMenuItem>
        </ContextMenu>
        <ContentList>
            <ContentListItemGrid v-for="item in fullSongList" :key="item.id" @click="onSongClick(item)" @contextmenu="onMiscClick($event, item)">
                <template v-slot:left>
                    <!-- <div class="icon"><fa-icon icon="play"/></div> -->
                </template>
                <div class="tracktitle" :class="{'disabled': !item.enabled}">{{item.tracktitle}}</div>
                <div class="artist" :class="{'disabled': !item.enabled}">{{item.artist}}</div>
                <template v-slot:right>
                    <div class="clickable-icon" @click.stop="() => openContextMenu($event, item)"><fa-icon icon="ellipsis-h"/></div>
                </template>
                <template v-slot:bottom>
                    <Tag class="tag" v-for="tag in item.tags" :key="tag.id">{{tag.name}}</Tag>
                    <div class="tag-plus-icon" @click.stop="openTagModal(item)"><fa-icon icon="plus"/></div>
                </template>
            </ContentListItemGrid>
        </ContentList>
        <Modal :show="displayTagModal" @close="closeTagModal()">
            <div class="tag-list-title">Current tags</div>
            <div class="tag-list">
                <Tag v-for="tag in currentTags" :key="tag.id" @click="untagSong(tag)">{{tag.name}}</Tag>
            </div>
            <div class="tag-list-title">Available tags</div>
            <div class="tag-list">
                <Tag v-for="tag in availableTags" :key="tag.id" @click="tagSong(tag)">{{tag.name}}</Tag>
            </div>
        </Modal>
    </div>
</template>

<script>
import ContentList from '@/components/ContentList.vue';
import ContentListItemGrid from '@/components/ContentListItemGrid.vue';
import ContextMenu from '@/components/ContextMenu.vue';
import ContextMenuItem from '@/components/ContextMenuItem.vue';
import Tag from '@/components/Tag.vue';
import Modal from '@/components/Modal.vue';
import { mapGetters, mapActions } from 'vuex'

export default {
    components: {
        ContentList,
        ContentListItemGrid,
        ContextMenu,
        ContextMenuItem,
        Tag,
        Modal
    },
    data: function() {
        return {
            loading: true,
            contextMenuPosX: 150,
            contextMenuPosY: 300,
            contextMenuSelected: null,
            showContextMenu: false,
            displayTagModal: false,
            tagModalItem: null,
            currentTags: [],
            availableTags: [],
        };
    },
    computed: {
        ...mapGetters(['fullSongList', 'tagList']),
    },
    watch: {
        tagModalItem: function() {
            if(this.tagModalItem == null || this.tagList == null) {
                this.currentTags = [];
                this.availableTags = [];
            } else {
                this.currentTags = this.tagList.filter((tag) => {
                    for(let i = 0; i < this.tagModalItem.tags.length; i++) {
                        if(tag.id === this.tagModalItem.tags[i].id) {
                            return true;
                        }
                    }
                    return false;
                });
                this.availableTags = this.tagList.filter((tag) => {
                    for(let i = 0; i < this.tagModalItem.tags.length; i++) {
                        if(tag.id === this.tagModalItem.tags[i].id) {
                            return false;
                        }
                    }
                    return true;
                });
            }
        }
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
        onContextMenuPlay: function() {
            this.onSongClick(this.contextMenuSelected);
        },
        openContextMenu: function(event, item) {
            this.contextMenuSelected = item;
            this.contextMenuPosX = event.clientX;
            this.contextMenuPosY = event.clientY;
            this.showContextMenu = true;
        },
        closeContextMenu: function() {
            this.contextMenuSelected = null;
            this.showContextMenu = false;
        },
        onContextMenuEnable: function() {
            fetch('/api/enable-songs', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(
                    [
                        {
                            "id": this.contextMenuSelected.id
                        }
                    ]
                )
            }).then((response) => {
                if(response.status !== 200) {
                    return;
                }
                return response.json();
            }).then((response) => {
                this.fetchFullSongList(); // TODO improve
            })
        },
        onContextMenuDisable: function() {
            fetch('/api/disable-songs', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(
                    [
                        {
                            "id": this.contextMenuSelected.id
                        }
                    ]
                )
            }).then((response) => {
                if(response.status !== 200) {
                    return;
                }
                return response.json();
            }).then((response) => {
                this.fetchFullSongList(); // TODO improve
            })
        },
        openTagModal: function(item) {
            this.displayTagModal = true;
            this.tagModalItem = item
        },
        closeTagModal: function() {
            this.displayTagModal = false;
            this.tagModalItem = null
        },
        tagSong: async function(tag) {
            await fetch('/api/tag-song', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(
                    {
                        "song_id": this.tagModalItem.id,
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
                        "song_id": this.tagModalItem.id,
                        "tag_id": tag.id
                    }
                )
            });
            this.fetchFullSongList();
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.container {

    .icon, .clickable-icon {
        font-size: 1.25rem;
        color: $list-item-icon-color;
        display: flex;
        justify-content: center;
        align-items: center;

        &.icon {
            width: 1rem;
        }

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

}

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

.tag-list {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}

.tag-list-title {
    margin-bottom: 0.5rem;
}
</style>
