<template>
    <div class="sidebar-item" @click="$emit('click', $event)">
        <div :class="{'selected': selected}" class="indicator"></div>
        {{title}}
    </div>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            required: true
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

.sidebar-item {
    position: relative;
    color: $text-color;
    user-select: none;
    cursor: pointer;
    padding: 0.5rem 1.25rem;
    font-size: 1rem;

    .indicator {
        background-color: $text-color;
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 0;
        height: 28px;
        transition: width 0.2s;

        &.selected {
            width: 6px;
        }
    }
}
</style>
