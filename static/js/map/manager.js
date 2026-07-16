class LayerManager{

    constructor(map){

        this.map=map;

        this.layers={};

    }

    register(name,layer){

        this.layers[name]=layer;

    }

    show(name){

        if(this.layers[name]){

            this.map.addLayer(

                this.layers[name]

            );

        }

    }

    hide(name){

        if(this.layers[name]){

            this.map.removeLayer(

                this.layers[name]

            );

        }

    }

    toggle(name){

        if(

            this.map.hasLayer(

                this.layers[name]

            )

        ){

            this.hide(name);

        }

        else{

            this.show(name);

        }

    }

    refresh(name){

        if(

            this.layers[name]?.refresh

        ){

            this.layers[name].refresh();

        }

    }

    refreshAll(){

        Object.values(

            this.layers

        ).forEach(layer=>{

            if(layer.refresh){

                layer.refresh();

            }

        });

    }

}

window.layerManager=null;