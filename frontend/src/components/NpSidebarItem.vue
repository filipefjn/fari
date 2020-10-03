<template>
    <div class="np-sidebar-item" @click="onClick($event)">
        <div class="np-sidebar-item-indicator" :class="{'np-sidebar-item-selected': selected}"></div>
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
        path: {
            type: String,
            required: true
        },
        names: {
            type: Array
        }
    },
    computed: {
        selected: function() {
            if(!this.names) {
                return false;
            }
            let matches = this.names.filter((name) => {
                if(this.$route.name == name) return true;
                else return false;
            });
            if(matches.length > 0) {
                return true;
            }
            return false;
        }
    },
    methods: {
        onClick: function(event) {
            if(this.$listeners.click) {
                this.$emit('click', event);
            } else {
                this.$router.push({path: this.path});
            }
        }
    }
}
</script>
