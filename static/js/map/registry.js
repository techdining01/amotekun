class LayerRegistry{

    constructor(){

        this.registry={};

    }

    add(name,config){

        this.registry[name]=config;

    }

    get(name){

        return this.registry[name];

    }

    all(){

        return Object.values(this.registry);

    }

}

window.layerRegistry=new LayerRegistry();