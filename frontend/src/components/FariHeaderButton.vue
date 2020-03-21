<template>
    <button class="header-button" :class="{'selected': selected, 'text': text}" v-on="listeners">
        <slot></slot>
    </button>
</template>

<script>
export default {
    props: {
        selected: {
            type: Boolean,
            default: false
        },
        text: {
            type: Boolean,
            default: false,
        }
    },
    computed: {
        listeners: function() {
            return Object.assign({}, this.$listeners);
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.header-button {
    display: flex;
    justify-content: center;
    align-items: center;
    border: none;
    outline: none;
    background-color: rgb(49, 49, 49);
    padding: 0.25rem 0.25rem;
    margin-left: 0.5rem;
    height: 1.75rem;
    min-width: 1.75rem;
    border-radius: 4px;
    overflow: hidden;
    cursor: pointer;
    color: rgb(116, 116, 116);
    text-transform: uppercase;
    font-weight: bold;
    font-size: 0.8rem;

    &:hover {
        background-color: rgb(58, 58, 58);
    }

    &:active {
        background-color: rgb(70, 70, 70);
    }

    &.selected {
        background-color: $primary;
        color: $primary-contrast;

        &:hover {
            background-color: $primary-dark;
        }

        &:active {
            background-color: $primary-darker;
        }
    }

    &.text {
        font-size: 0.7rem;
        padding: 0.25rem 0.75rem;
    }
}

</style>
