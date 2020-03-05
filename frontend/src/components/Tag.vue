<template>
    <div class="tag">
        <slot></slot>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.tag {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: $primary;
    color: black;
    text-transform: uppercase;
    font-weight: bold;
    font-size: 0.7rem;
    border-radius: 6px;
    border: none;
    padding: 0.25rem 0.5rem;
    margin: 0.1rem 0.25rem;
    box-shadow: $context-menu-shadow;

    &:first-child {
        margin-left: 0;
    }
}
</style>
