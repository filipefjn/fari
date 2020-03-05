<template>
    <div class="container" @click="$emit('click', $event)" @contextmenu.prevent="$emit('contextmenu', $event)">
        <div class="list-item">
            <slot name="left"></slot>
            <div class="grid">
                <slot></slot>
            </div>
            <slot name="right"></slot>
        </div>
        <div class="bottom">
            <slot name="bottom"></slot>
        </div>
    </div>

</template>

<script>
export default {

}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.container {
    display: grid;
    grid-template-columns: 100%;
    cursor: pointer;
    border-top: solid 2px $list-item-line-color;

    &:hover {
        background-color: $list-item-hover-bgcolor;
    }

    &:last-child {
        border-bottom: solid 2px $list-item-line-color;
    }

    .list-item {
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
    }

    .bottom {
        // padding-top: $list-item-hor-padding;
        // padding-bottom: $list-item-hor-padding;
        padding-left: 1rem;
        padding-right: 1rem;
        display: flex;

    }
}


</style>
