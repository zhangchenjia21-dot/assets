import com.google.gson.*;
import com.mojang.serialization.JsonOps;
import net.minecraft.SharedConstants;
import net.minecraft.server.Bootstrap;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.EmptyBlockGetter;
import net.minecraft.core.BlockPos;
import java.nio.file.*;
/** 仅查询 26.2 方块状态的无实体上下文碰撞形状；不打开任何世界，也不宣称实测玩家移动。 */
public class 原生碰撞形状 {
 public static void main(String[] args)throws Exception {
  SharedConstants.tryDetectVersion();Bootstrap.bootStrap();var input=JsonParser.parseString(Files.readString(Path.of(args[0]))).getAsJsonObject();var out=new JsonObject();var rows=new JsonObject();
  for(var value:input.getAsJsonArray("palette")){String s=value.getAsString();var j=new JsonObject();int k=s.indexOf('[');j.addProperty("Name",k<0?s:s.substring(0,k));if(k>=0){var props=new JsonObject();for(String pair:s.substring(k+1,s.length()-1).split(",")){String[] p=pair.split("=");props.addProperty(p[0],p[1]);}j.add("Properties",props);}
   var state=BlockState.CODEC.parse(JsonOps.INSTANCE,j).getOrThrow();var boxes=new JsonArray();for(var a:state.getCollisionShape(EmptyBlockGetter.INSTANCE,BlockPos.ZERO).toAabbs()){var box=new JsonArray();for(double v:new double[]{a.minX,a.minY,a.minZ,a.maxX,a.maxY,a.maxZ})box.add(v);boxes.add(box);}rows.add(s,boxes);
  }
  out.addProperty("no_world_opened",true);out.addProperty("runtime",SharedConstants.getCurrentVersion().name());out.addProperty("context","EmptyBlockGetter / default collision context; not player movement simulation");out.add("shapes",rows);Files.writeString(Path.of(args[1]),new Gson().toJson(out));System.out.println("shape states="+rows.size());System.exit(0);
 }
}
