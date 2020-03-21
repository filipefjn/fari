<template>
    <div class="list-item" @click="$emit('click', $event)" :class="{'no-siblings': noSiblings, 'selected': selected}">
        <slot></slot>
    </div>
</template>

<script>
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

    &:last-child:not(.no-siblings) {
        border-bottom: solid 2px $list-item-line-color;
    }

    &:hover {
        background-color: $list-item-hover-bgcolor;
    }

    &.selected {
        color: $primary;
    }
}
</style>
