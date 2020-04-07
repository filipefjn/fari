<template>
    <FariContextMenu
        v-bind="$attrs"
        v-on="listeners"
        :show="show"
        :posX="posX"
        :posY="posY"
    >
        <slot name="contextmenu">
            <div class="rating-list">
                <img src="@/assets/rating-none.svg" @click.stop="changeRatingTo(0)">
                <img src="@/assets/rating-1.svg" @click.stop="changeRatingTo(1)">
                <img src="@/assets/rating-2.svg" @click.stop="changeRatingTo(2)">
                <img src="@/assets/rating-3.svg" @click.stop="changeRatingTo(3)">
                <img src="@/assets/rating-4.svg" @click.stop="changeRatingTo(4)">
                <img src="@/assets/rating-5.svg" @click.stop="changeRatingTo(5)">
            </div>
        </slot>
    </FariContextMenu>
</template>

<script>
import FariContextMenu from "@/components/FariContextMenu.vue";
import FariContextMenuItem from "@/components/FariContextMenuItem.vue";

export default {
    props: {
        posX: Number,
        posY: Number,
        show: {
            type: Boolean,
            required: true
        },
        song: {
            type: Object,
            required: true,
        }
    },
    inheritAttrs: false,
    computed: {
        listeners: function() {
            return Object.assign({}, this.$listeners);
        }
    },
    components: {
        FariContextMenu,
        FariContextMenuItem
    },
    methods: {
        changeRatingTo: function(rating) {
            fetch('/api/change-song-rating', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    song_id: this.song.id,
                    rating: rating
                })
            }).then(async (response) => {
                if(response.status === 200) {
                    this.$emit('change');
                }
                this.$emit('close');
            });
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.rating-list {
    display: flex;
    flex-direction: row;

    & > * {
        height: 2rem;
        width: 2rem;
        margin: 0.25rem 0.1rem;
        padding: 0.5rem;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.1s;

        &:hover {
            background-color: $context-menu-hover-bgcolor;
        }
    }
}

</style>

