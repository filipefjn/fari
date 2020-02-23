<template>
    <div class="container">
        <ContextMenu :posX="contextMenuPosX" :posY="contextMenuPosY" :show="showContextMenu" @close="closeContextMenu()" @mouseleave="closeContextMenu()">
            <ContextMenuItem @click="onContextMenuPlay()">Play</ContextMenuItem>
            <!-- <ContextMenuItem>Play next</ContextMenuItem> -->
            <!-- <ContextMenuItem>Queue song</ContextMenuItem> -->
            <ContextMenuItem>Disable</ContextMenuItem> <!-- TODO: implement -->
        </ContextMenu>
        <ContentList>
            <ContentListItemGrid v-for="item in songs" :key="item.id" @click="onSongClick(item)" @contextmenu="onMiscClick($event, item)">
                <template v-slot:left>
                    <!-- <div class="icon"><fa-icon icon="play"/></div> -->
                </template>
                <div class="tracktitle" :class="{'disabled': item.disabled}">{{item.tracktitle}}</div>
                <div class="artist">{{item.artist}}</div>
                <template v-slot:right>
                    <div class="clickable-icon" @click.stop="() => openContextMenu($event, item)"><fa-icon icon="ellipsis-h"/></div>
                </template>
            </ContentListItemGrid>
        </ContentList>
    </div>
</template>

<script>
import ContentList from '@/components/ContentList.vue';
import ContentListItemGrid from '@/components/ContentListItemGrid.vue';
import ContextMenu from '@/components/ContextMenu.vue';
import ContextMenuItem from '@/components/ContextMenuItem.vue';

export default {
    components: {
        ContentList,
        ContentListItemGrid,
        ContextMenu,
        ContextMenuItem
    },
    data: function() {
        return {
            loading: true,
            songs: [],
            contextMenuPosX: 150,
            contextMenuPosY: 300,
            contentMenuSelected: null,
            showContextMenu: false,
        };
    },
    mounted: function() {
        this.$store.dispatch('setHeaderInfo', {
            title: "All Songs",
        });
        this.fetchAllSongs();
    },
    methods: {
        fetchAllSongs: function() {
            fetch('/api/all-songs', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                }
            }).then((response) => {
                return response.json();
            }).then((response) => {
                this.songs = response;
            })
        },
        onSongClick: async function(song) {
            if(song.disabled) {
                console.log("disabled song clicked!");
                return;
            }
            let queue = [];
            let queuePlayIndex = 0;
            for(let i = 0; i < this.songs.length; i++) {
                if(song.disabled) {
                    return;
                }
                if(this.songs[i].id == song.id) {
                    queuePlayIndex = i;
                }
                queue.push({
                    path: this.songs[i].path
                });
            }
            await this.$store.dispatch('setQueue', queue);
            await this.$store.dispatch('playFromQueue', queuePlayIndex);
        },
        onContextMenuPlay: function() {
            this.onSongClick(this.contentMenuSelected);
        },
        openContextMenu: function(event, item) {
            this.contentMenuSelected = item;
            this.contextMenuPosX = event.clientX;
            this.contextMenuPosY = event.clientY;
            this.showContextMenu = true;
        },
        closeContextMenu: function() {
            this.contentMenuSelected = null;
            this.showContextMenu = false;
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
</style>
