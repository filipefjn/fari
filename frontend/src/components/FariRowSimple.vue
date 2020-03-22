<template>
    <div class="list-item"
        @click="$emit('click', $event)"
        :class="{'no-siblings': noSiblings, 'selected': selected, 'narrow': listParams.isNarrow}"
    >
        <slot></slot>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    props: {
        noSiblings: {
            type: Boolean,
            default: false
        },
        selected: {
            type: Boolean,
            default: false
        }
    },
    computed: {
        ...mapGetters(['listParams'])
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.list-item {
    padding-top: $list-item-hor-padding;
    padding-bottom: $list-item-hor-padding;
    padding-left: 1rem;
    padding-right: 1rem;
    border-top: solid 2px $list-item-line-color;
    color: $text-color;
    cursor: pointer;
    display: flex;
    align-items: center;
    user-select: none;

    &.narrow {
        border-top-width: 1px;
        font-size: 0.75rem;
        padding: 0.5rem 0.25rem;
    }

    &:last-child:not(.no-siblings) {
        border-bottom: solid 2px $list-item-line-color;

        &.narrow {
            border-bottom-width: 1px;
        }
    }

    &:hover {
        background-color: $list-item-hover-bgcolor;
    }

    &.selected {
        color: $primary;
    }
}
</style>
