/*http://msdn.microsoft.com/en-us/library/bb509632.aspx*/

/**
* Aligns sizes to suit HLSL.
* @param range The value or range of values that need to be aligned.
* Parses:
* /^\s*(\d+)\s*$/ (as number, eg 3)
* /^\s*(\d+)\s*\[\s*(\d+)\s*\]\s*$/ (as array, eg 3[2]) 
* /^\d+(\s*,\s*\d+)*$/ (as struct components, eg 1,3,4).
* @return The aligned sizes.
* @customfunction
*/
function hlslAligner(range) {
  return bufferAligner(range, 4, 16, 0,"verbose");
}
var debug = [];
/**
* Aligns sizes.
* @param {string[]} sizes The elements that needs to be aligned.
* Parses:
* /^\s*(\d+)\s*$/ (as number)
* /^\s*(\d+)\s*\[\s*(\d+)\s*\]\s*$/ (as array) 
* /^\d+(\s*,\s*\d+)*$/ (as struct).
* @param {number} size_t Size that is read at a time.
* @param {number} chunksize_t Data must not cross these boundaries.
* @param {number} align Start offset.
* @param {string=} format "verbose" for verbose output 
* @return The aligned sizes.
* @customfunction
*/
function bufferAligner(sizes, size_t, chunksize_t, align, format) {
  var aligns = [];
  
  var numberpattern = /^\s*(\d+)\s*$/;
  var arraypattern = /^\s*(\d+)\s*\[\s*(\d+)\s*\]\s*$/;
  var structpattern = /^(\d)+(\s*,\s*\d+)+$/;
  for (var i = 0; i < sizes.length; i++) {//row
    var size = sizes[i];
    if (typeof size !== "string") { size = size.toString(); }
    if (size == "") break;
    var number = numberpattern.exec(size);
    var array = arraypattern.exec(size);
    var struct = structpattern.exec(size);
    if (number != null) 
      //NUMBER
    {
      size = parseInt(size);
      
      align = aligner(size,size_t,chunksize_t,align);
      
      if(format == "verbose") {
        aligns.push("[FieldOffset(" + align.toString() + ")]");
      } else {
        aligns.push(align.toString()); 
      }
      
      align += size;
      
    } else if (array !== null) 
      //ARRAY
    { 
      size = parseInt(array[1]);
      var len = parseInt(array[2]);
      
      //Warning text...
      var str = "\t//";
      if (size < chunksize_t) { size = chunksize_t; str += "(not chunk-aligned, "+chunksize_t.toString()+"-byte struct assumed. alt: aggressive packing)"; }
      if (size % chunksize_t !== 0) { throw "not chunk-aligned: " + size.toString() + "%" + chunksize_t.toString() + "≠0"; }
      
      //"Arrays are not packed in HLSL by default." 
      align += ((align%chunksize_t) == 0) ? 0 : chunksize_t - (align%chunksize_t);
      
      if(format == "verbose") {
        aligns.push("[FieldOffset(" + align.toString() + "), MarshalAs(UnmanagedType.ByValArray, SizeConst=" + len.toString() + ")]" + str)
      } else {
        aligns.push(align.toString());
      }
      
      align += size * len;
      
    } else if (struct !== null) 
      //STRUCT
    {
      struct = size.split(/\s*,\s*/);
      var structadd = bufferAligner(struct,size_t,chunksize_t,0);
      size = parseInt(structadd[0]);
      align = aligner(size,size_t,chunksize_t,align);
      if(format == "verbose") {
        structadd = bufferAligner(struct,size_t,chunksize_t,0,"verbose");
        structadd.unshift("[FieldOffset("+align.toString()+")] internal type:");
      } else {
        structadd.unshift(align.toString() + " internal type:");
      }
      aligns.push(structadd);
      align += size;
    } else {throw "Unsupported input: " + size; }
    
  }
  
  if(align > chunksize_t) 
    //Aligns to chunksize_t if it crosses a chunksize_t boundary.
  {
    align += ((align%chunksize_t) == 0) ? 0 : chunksize_t - (align%chunksize_t);
  }
  
  if(format == "verbose") {
    aligns.unshift("[StructLayout(LayoutKind.Explicit, Size=" + align.toString() + " /* = 16*" + (align / 16).toString() + "*/)]");
  } else {
    aligns.unshift(align.toString()); 
  }
  return aligns;
}
function aligner(size, size_t, chunksize_t, align) {
  if(isNaN(size) || isNaN(size_t) || isNaN(chunksize_t) || isNaN(align)) { 
    throw debug + "Unsupported format: aligner(" + size+","+size_t+","+chunksize_t+","+align+");"; 
  }
  /*#pragma pack( [ show ] | [ push | pop ] [, identifier ] , n  )
  The alignment of a member will be on a boundary that is either a multiple of n
  or a multiple of the size of the member, whichever is smaller.*/
  var minsize_t = (size < size_t) ? size : size_t;
  if((align%chunksize_t) + size <= chunksize_t) 
    // if it fits within the chunk
  {
    align += ((align%minsize_t) == 0) ? 0 : minsize_t - (align%minsize_t);
  } else 
    // pack data so that it does not cross a chunksize_t-byte boundary
  {
    align += ((align%chunksize_t) == 0) ? 0 : chunksize_t - (align%chunksize_t);
  }
  return align;
}
