<template>
    <div class="icon" :class="{'small': small, 'narrow': listParams.isNarrow}">
        <slot></slot>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    props: {
        small: {
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

.icon {
    margin-right: 1rem;
    font-size: 1.25rem !important;
    width: 1rem;
    color: $list-item-icon-color;
    display: flex;
    justify-content: center;
    align-items: center;

    &.narrow {
        font-size: 1rem !important;
        margin-right: 0.5rem !important;
    }

    &.small {
        font-size: 1rem !important;

        &.narrow {
            font-size: 0.75rem !important;
        }
    }
}
</style>
