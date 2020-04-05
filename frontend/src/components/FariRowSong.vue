<template>
    <div class="song-row"
        :class="{'disabled': !song.enabled, 'no-siblings': noSiblings, 'narrow': listParams.isNarrow}"

        @contextmenu.prevent="$emit('contextmenu', $event)">

        <!-- song info -->
        <div class="song-row-info" :class="{'narrow': listParams.isNarrow}" v-if="song" @click="$emit('click', $event)">
            <slot name="left"></slot>
            <div class="song-info">
                <div class="tracknumber"
                    :class="{'disabled': !song.enabled, 'current': currentSong}"
                    v-show="showTracknumber"
                >{{song.tracknumber}}</div>
                <div class="rating" @click.stop="() => openRatingMenu($event)">
                    <img class="rating-image" v-if="song.rating === 0" src="@/assets/rating-none.svg">
                    <img class="rating-image" v-if="song.rating === 1" src="@/assets/rating-1.svg">
                    <img class="rating-image" v-if="song.rating === 2" src="@/assets/rating-2.svg">
                    <img class="rating-image" v-if="song.rating === 3" src="@/assets/rating-3.svg">
                    <img class="rating-image" v-if="song.rating === 4" src="@/assets/rating-4.svg">
                    <img class="rating-image" v-if="song.rating === 5" src="@/assets/rating-5.svg">
                </div>
                <div class="tracktitle"
                    :class="{'disabled': !song.enabled, 'current': currentSong}"
                >{{song.tracktitle}}</div>
                <div class="artist"
                    :class="{'disabled': !song.enabled, 'current': currentSong}"
                >{{song.artist}}</div>
            </div>
            <div class="clickable-icon" @click.stop="() => openContextMenu($event)"><fa-icon icon="ellipsis-h"/></div>
        </div>

        <!-- song tags -->
        <div class="song-row-tags" :class="{'narrow': listParams.isNarrow}" v-if="song && listParams.showTags" @click="$emit('click', $event)">
            <FariTag class="tag" v-for="tag in song.tags" :key="tag.id">{{tag.name}}</FariTag>
            <div class="tag-plus-icon" @click.stop="openFariModalTag()"><fa-icon icon="tags"/></div>
        </div>

        <!-- rating menu -->
        <FariRatingMenu
            :show="displayRatingMenu"
            :posX="ratingMenuPosX"
            :posY="ratingMenuPosY"
            :song="song"
            @close="closeRatingMenu()"
            @mouseleave="closeRatingMenu()"
            @change="$emit('change')"/>

        <!-- context menu -->
        <FariContextMenu
            :show="displayContextMenu"
            :posX="contextMenuPosX"
            :posY="contextMenuPosY"
            @close="closeContextMenu()"
            @mouseleave="closeContextMenu()"
        >
            <slot name="contextmenu">
                <FariContextMenuItem @click.stop="contextMenuPlaySong()">Play</FariContextMenuItem>
                <FariContextMenuItem @click.stop="openFariModalTag()">Edit tags</FariContextMenuItem>
                <FariContextMenuItem v-if="!song.enabled" @click.stop="contextMenuEnableSong()">Enable</FariContextMenuItem>
                <FariContextMenuItem v-if="song.enabled" @click.stop="contextMenuDisableSong()">Disable</FariContextMenuItem>
            </slot>
        </FariContextMenu>

        <!-- tag modal -->
        <FariModalTag
            v-if="displayFariModalTag"
            :song="song"
            @close="closeFariModalTag()"
            @change="onTagChange()"/>
    </div>
</template>

<script>
import FariContextMenu from '@/components/FariContextMenu.vue';
import FariContextMenuItem from '@/components/FariContextMenuItem.vue';
import FariTag from '@/components/FariTag.vue';
import FariModalTag from '@/components/FariModalTag.vue';
import FariRatingMenu from '@/components/FariRatingMenu.vue';

import { mapGetters, mapActions } from 'vuex';

export default {
    props: {
        song: {
            type: Object,
            required: true
        },
        showTags: {
            type: Boolean
        },
        noSiblings: {
            type: Boolean,
            default: false
        },
        showTracknumber: {
            type: Boolean,
            default: false
        },
        showRating: {
            type: Boolean,
            default: false,
        }
    },
    components: {
        FariContextMenu,
        FariContextMenuItem,
        FariTag,
        FariModalTag,
        FariRatingMenu
    },
    data: function() {
        return {
            contextMenuPosX: 150,
            contextMenuPosY: 300,
            displayContextMenu: false,
            displayFariModalTag: false,
            ratingMenuPosX: 150,
            ratingMenuPosY: 150,
            displayRatingMenu: false
        }
    },
    computed: {
        ...mapGetters(['tagList', 'listParams', 'queuePlaySongId']),
        currentSong: function() {
            if(this.queuePlaySongId == this.song.id) {
                return true;
            } else {
                return false
            }
        }
    },
    methods: {
        openContextMenu: function(event) {
            this.displayContextMenu = true;
            this.contextMenuPosX = event.clientX;
            this.contextMenuPosY = event.clientY;
        },
        closeContextMenu: function() {
            this.displayContextMenu = false;
        },
        openRatingMenu: function(event) {
            this.displayRatingMenu = true;
            this.ratingMenuPosX = event.clientX;
            this.ratingMenuPosY = event.clientY;
        },
        closeRatingMenu: function(event) {
            this.displayRatingMenu = false;
        },
        openFariModalTag: function() {
            this.displayFariModalTag = true;
        },
        closeFariModalTag: function() {
            this.displayFariModalTag = false;
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
                this.$emit('change');
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
                this.$emit('change');
            });
            this.closeContextMenu();
        },
        onTagChange: function() {
            this.$emit('change');
        }
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

    &.narrow {
        border-top-width: 1px;
        font-size: 0.75rem;
    }

    &:hover {
        background-color: $list-item-hover-bgcolor;
    }

    &:last-child:not(.no-siblings) {
        border-bottom: solid 2px $list-item-line-color;

        &.narrow {
            border-bottom-width: 1px;
        }
    }

    &.disabled {
        cursor: not-allowed;
    }

    .song-row-info {
        padding-left: 1rem;
        padding-right: 1rem;
        height: 3rem;
        color: $text-color;

        &.narrow {
            height: 2rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }

        display: flex;
        align-items: center;
        user-select: none;

        .grid {
            display: grid;
            grid-template-columns: 10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
            flex-grow: 1;
            flex-shrink: 1;
        }

        .song-info {
            display: flex;
            flex-direction: row;
            justify-content: space-around;
            flex-grow: 1;
            flex-shrink: 1;
            overflow: hidden;
        }

        .tracknumber, .tracktitle, .artist {
            display: flex;
            align-items: center;
        }

        .tracknumber {
            // flex: 1;
            width: 3rem;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
            justify-content: flex-end;
            padding-right: 1.5rem;
        }

        .rating {
            margin-right: 1.25rem;
            // color: #cecece;
            padding: $list-item-clickable-icon-padding;
            border-radius: 6px;

            display: flex;
            justify-content: center;
            align-items: center;

            &:hover {
                background-color: $list-item-icon-hover-bgcolor;
            }

            .rating-image {
                margin-top: 1px;
                height: 1rem;
            }
        }

        .tracktitle {
            grid-column: 1 / 7;
            flex: 10;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
            padding-right: 1.5rem;
            justify-content: flex-start;
        }

        .artist {
            grid-column: 7 / 11;
            flex: 8;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
            justify-content: flex-start;
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

        &.narrow {
            padding-left: 0.25rem;
            padding-right: 0.25rem;
        }
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

.narrow .clickable-icon {
    font-size: 1rem;
    margin-top: -0.5rem;
    margin-bottom: -0.5rem;
    padding: 0.25rem;
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
