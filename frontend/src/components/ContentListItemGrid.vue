<template>
    <div class="list-item" @click="$emit('click', $event)" @contextmenu.prevent="$emit('contextmenu', $event)">
        <slot name="left"></slot>
        <div class="grid">
            <slot></slot>
        </div>
        <slot name="right"></slot>
    </div>
</template>

<script>
export default {

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

    .grid {
        display: grid;
        grid-template-columns: 10% 10% 10% 10% 10% 10% 10% 10% 10% 10%;
        flex-grow: 1;
        flex-shrink: 1;
    }

    &:last-child {
        border-bottom: solid 2px $list-item-line-color;
    }

    &:hover {
        background-color: $list-item-hover-bgcolor;
    }
}
</style>
