<template>
    <div class="list-item" @click="$emit('click', $event)">
        <slot></slot>
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

    &:last-child {
        border-bottom: solid 2px $list-item-line-color;
    }

    &:hover {
        background-color: $list-item-hover-bgcolor;
    }
}
</style>
