<template>
    <div class="input-wrapper">
        <input class="input-field"
            :value="computedValue"
            :placeholder="placeholder"
            :type="type"
            ref="inputField"
            @input="onInput()">
        <button
            v-for="button in buttons"
            :key="button.text"
            @click="$emit(button.emit, $event)"
            class="input-button"
        >{{button.text}}</button>
    </div>
</template>

<script>
export default {
    props: {
        buttons: {
            /*
                must be an array of objects:
                [
                    {
                        text: String,
                        emit: String
                    }
                ]
            */
            type: Array,
            default: []
        },
        placeholder: {
            type: String,
            default: ""
        },
        value: {
            type: String
        },
        type: {
            type: String,
            default: "text"
        }
    },
    data: function() {
        return {
            insideValue: ""
        };
    },
    computed: {
        computedValue: function() {
            if(this.value === undefined || this.value === null) {
                return this.insideValue;
            } else {
                return this.value;
            }
        }
    },
    methods: {
        onInput: function() {
            this.$emit('input', this.$refs.inputField.value);
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.input-wrapper {

    display: flex;
    flex-direction: row;
    align-items: center;
    padding-top: 0.25rem;
    padding-bottom: 0.25rem;

    .input-field {
        background-color: transparent;
        border-radius: 6px;

        margin: 0;

        padding: 0.4rem 1rem;
        border: none;

        padding-left: 0.75rem;
        padding-right: 0.75rem;

        border: 2px solid $primary;
        border-right: none;
        color: $text-color;
        box-shadow: inset 0 0 7px rgba(0,0,0,0.2);

        &::placeholder {
            color: rgb(179, 179, 179);
        }
    }

    .input-button {
        border-radius: 6px;
        border: none;
        padding-left: 0.75rem;
        padding-right: 0.75rem;
        cursor: pointer;
        background-color: $primary;
        font-weight: bold;

        &:hover {
            background-color: $primary-light;
        }

        &:active {
            background-color: $primary-lighter;
        }

        &:not(:first-of-type) {
            margin-left: 2px;
        }
    }

    .input-separator {
        // border: 2px solid $primary;
        border-left: none;
        border-right: none;
        background-color: transparent;
        width: 2px;
    }

    & > * {
        height: 2rem !important;
    }

    & > *:not(:first-child) {
        border-top-left-radius: 0 !important;
        border-bottom-left-radius: 0 !important;
        // margin-left: 0 !important;
    }

    & > *:not(:last-child) {
        border-top-right-radius: 0 !important;
        border-bottom-right-radius: 0 !important;
        // margin-right: 0 !important;
    }
}

</style>
