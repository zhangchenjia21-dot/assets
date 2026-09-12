package probe;
import net.fabricmc.loader.api.entrypoint.PreLaunchEntrypoint;
import net.minecraft.SharedConstants;
import net.minecraft.server.Bootstrap;
import net.minecraft.core.registries.BuiltInRegistries;
import fi.dy.masa.litematica.schematic.LitematicaSchematic;
import com.google.gson.*;
import java.nio.file.*;
import java.util.*;

/** 独立 Fabric preLaunch 只初始化方块注册表并读取文件；退出早于游戏客户端和存档创建。 */
public final class 投影加载探针 implements PreLaunchEntrypoint {
 public void onPreLaunch(){try{
  SharedConstants.tryDetectVersion();Bootstrap.bootStrap();
  Path evidence=Path.of(System.getProperty("v6.evidence"));
  // Litematica 配置静态初始化只需客户端目录。探针提供这一只读上下文，避免启动窗口/账号/世界。
  var unsafeField=sun.misc.Unsafe.class.getDeclaredField("theUnsafe");unsafeField.setAccessible(true);var unsafe=(sun.misc.Unsafe)unsafeField.get(null);
  var minecraftClass=net.minecraft.client.Minecraft.class;var context=unsafe.allocateInstance(minecraftClass);
  var directory=minecraftClass.getDeclaredField("gameDirectory");directory.setAccessible(true);directory.set(context,Path.of(".").toAbsolutePath().toFile());
  var instance=minecraftClass.getDeclaredField("instance");instance.setAccessible(true);instance.set(null,context);
  fi.dy.masa.litematica.world.SchematicWorldHandler.INSTANCE.setDynamicRegistryManager(net.minecraft.core.RegistryAccess.fromRegistryOfRegistries(BuiltInRegistries.REGISTRY));
  JsonArray results=new JsonArray();
  for(String file:new String[]{"京町家修复.litematic","roundtrip.litematic","multi-region-fixture.litematic","building-states-fixture.litematic"}){
   System.out.println("NATIVE_LOADING "+file);
   LitematicaSchematic schematic=LitematicaSchematic.createFromFile(evidence,file);
   if(schematic==null)throw new AssertionError("LITEMATICA_LOAD_FAILED: "+file);
   JsonArray states=new JsonArray();int occupied=0;JsonArray regions=new JsonArray();
   for(String name:new TreeSet<>(schematic.getAreaSizes().keySet())){
    var c=schematic.getSubRegionContainer(name);if(c==null)throw new AssertionError("Missing container "+name);
    var size=c.getSize();var position=schematic.getSubRegionPosition(name);var signed=schematic.getAreaSize(name);
    JsonObject region=new JsonObject();region.addProperty("name",name);region.addProperty("size",size.toString());region.addProperty("position",position.toString());regions.add(region);
    for(int y=0;y<size.getY();y++)for(int z=0;z<size.getZ();z++)for(int x=0;x<size.getX();x++){
     var state=c.get(x,y,z);if(state.isAir())continue;occupied++;
     JsonObject row=new JsonObject();row.addProperty("region",name);row.addProperty("x",position.getX()+Math.min(0,signed.getX()+1)+x);row.addProperty("y",position.getY()+Math.min(0,signed.getY()+1)+y);row.addProperty("z",position.getZ()+Math.min(0,signed.getZ()+1)+z);
     String id=BuiltInRegistries.BLOCK.getKey(state.getBlock()).toString();TreeMap<String,String> properties=new TreeMap<>();state.getValues().forEach(p->properties.put(p.property().getName(),p.valueName()));
     row.addProperty("state",id+(properties.isEmpty()?"":"["+String.join(",",properties.entrySet().stream().map(e->e.getKey()+"="+e.getValue()).toList())+"]"));states.add(row);
    }
   }
   JsonObject result=new JsonObject();result.addProperty("file",file);result.addProperty("status","PASS");result.addProperty("regions",schematic.getSubRegionCount());result.addProperty("occupied",occupied);result.add("region_details",regions);result.add("states",states);results.add(result);
  }
  Files.writeString(evidence.resolve("native-litematica-load.json"),new GsonBuilder().setPrettyPrinting().create().toJson(results));
  System.out.println("V6A_NATIVE_LITEMATICA_LOAD_PASS_NO_WORLD_OPENED");System.exit(0);
 }catch(Throwable e){e.printStackTrace();System.exit(1);}}
}
